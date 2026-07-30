#!/usr/bin/env python3

"""
Post schema validation for WGTS RNA workflows

Performs the following steps:
* Validate engine parameters:
  - Confirm projectId resolves to a valid ICAv2 project
  - Confirm outputUri starts with the project S3 prefix
  - Confirm logsUri starts with the project S3 prefix
  - Confirm outputUri ends with /<analysis-midfix>/<workflow-name>/<portal-run-id>/
  - Confirm logsUri ends with /logs/<workflow-name>/<portal-run-id>/
  - Confirm pipelineId is accessible in the specified projectId

* Validate inputs:
  - Skip URIs in reference data bucket, test data bucket, or project prefix
  - For file URIs (no trailing /): confirm exists in Filemanager
  - For folder URIs (trailing /): confirm at least 1 file exists under that prefix
  - For URIs not in ref/test/project-prefix: confirm accessible in ICA project context

* On failure: write descriptive comment(s) and return {"isValid": false}
* On success: return {"isValid": true}
"""

# Imports
from pathlib import Path
from typing import Dict, Tuple, cast, List
import logging
from os import environ
from time import sleep
from urllib.parse import urlparse

# Wrapica imports
from libica.openapi.v3 import ApiException
from wrapica.project_data import coerce_data_id_or_uri_to_project_data_obj, get_project_data_obj_by_id
from wrapica.storage_configuration import get_s3_key_prefix_by_project_id
from wrapica.project_pipelines import get_project_pipeline_obj
from wrapica.project import get_project_obj_from_project_id

# Layer imports
from orcabus_api_tools.workflow import add_comment_to_workflow_run, get_workflow_run
from orcabus_api_tools.filemanager import get_s3_object_id_from_s3_uri, list_files_recursively
from orcabus_api_tools.filemanager.errors import S3FileNotFoundError

from icav2_tools import set_icav2_env_vars

# Globals
WORKFLOW_NAME_ENV_VAR = "WORKFLOW_NAME"
TEST_BUCKET_ENV_VAR = "TEST_DATA_BUCKET_NAME"
REF_DATA_BUCKET_ENV_VAR = "REF_DATA_BUCKET_NAME"
# Get test / ref env var values
TEST_BUCKET = environ[TEST_BUCKET_ENV_VAR]
REF_DATA_BUCKET = environ[REF_DATA_BUCKET_ENV_VAR]
# Get workflow env vars as values
WORKFLOW_NAME = environ[WORKFLOW_NAME_ENV_VAR]
COMMENT_AUTHOR = f"{WORKFLOW_NAME}-workflow-validation-service"
# Midfixes
ANALYSIS_MIDFIX = "analysis"
LOGS_MIDFIX = "logs"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Comment formatting constants
MAX_COMMENT_LENGTH = 1024
TRUNCATION_SUFFIX = "\n... [truncated, see execution ARN for full detail]"


def _format_comment_with_arn(body: str, execution_arn: str) -> str:
    """
    Append the execution ARN footer to a comment and enforce the 1024 char limit.
    """
    footer = f"---\nStep Functions Execution: {execution_arn}"
    full_comment = f"{body}\n{footer}"

    if len(full_comment) > MAX_COMMENT_LENGTH:
        available = MAX_COMMENT_LENGTH - len(footer) - len(TRUNCATION_SUFFIX) - 1
        full_comment = f"{body[:available]}{TRUNCATION_SUFFIX}\n{footer}"

    return full_comment


def validate_engine_parameters(
        engine_parameters: Dict,
        workflow_run_id: str,
        project_prefix: str
) -> Tuple[bool, str]:
    """
    Validate the engine parameters.
    :param engine_parameters: The engine parameters to validate.
    :param workflow_run_id: The workflow run ID
    :param project_prefix: The project prefix
    :return: A tuple of (is_valid, comment)
    """
    # Get the project id
    project_id = cast(str, engine_parameters.get("projectId"))

    # Confirm that the outputUri and logsUri are a subset of the project prefix
    output_uri = engine_parameters.get("outputUri", "")
    logs_uri = engine_parameters.get("logsUri", "")
    pipeline_id = engine_parameters.get("pipelineId", "")

    # Assert project id
    if project_id is None:
        return False, "projectId is not set"
    try:
        get_project_obj_from_project_id(project_id)
    except ApiException:
        return False, f"Cannot find project id {project_id}"

    # Validate the uris are correct
    if not output_uri.startswith(project_prefix):
        return False, f"outputUri '{output_uri}' is not in the project context '{project_prefix}'"
    if not logs_uri.startswith(project_prefix):
        return False, f"logsUri '{logs_uri}' is not in the project context '{project_prefix}'"

    # Confirm the pipeline is in the project
    try:
        _ = get_project_pipeline_obj(
            project_id=project_id,
            pipeline_id=pipeline_id,
        )
    except ValueError as e:
        return False, f"The pipeline {pipeline_id} cannot be found in the project {project_id}"

    # Get the portal run id from the workflow run id
    portal_run_id = get_workflow_run(workflow_run_id)['portalRunId']

    # Confirm that the output uri ends with /<analysis-midfix>/<workflow-name>/<portal-run-id>/
    if not output_uri.endswith(f"/{ANALYSIS_MIDFIX}/{WORKFLOW_NAME}/{portal_run_id}/"):
        return False, f"outputUri '{output_uri}' does not end with '/{ANALYSIS_MIDFIX}/{WORKFLOW_NAME}/{portal_run_id}/'"
    # Confirm that the logs uri ends with /logs/<workflow-name>/<portal-run-id>/
    if not logs_uri.endswith(f"/{LOGS_MIDFIX}/{WORKFLOW_NAME}/{portal_run_id}/"):
        return False, f"logsUri '{logs_uri}' does not end with '/{LOGS_MIDFIX}/{WORKFLOW_NAME}/{portal_run_id}/'"

    return True, ""


def validate_inputs(
        inputs: Dict,
        project_id: str,
        project_prefix: str,
) -> Tuple[bool, str]:
    """
    Validate the inputs.

    Performs two-phase validation:
    1. Filemanager existence check — confirms file/folder URIs exist at the S3 level
       (excludes reference data bucket URIs since they are not indexed by the Filemanager)
    2. ICA project context check — confirms URIs outside of ref/test/project-prefix
       are linked to the project

    :param inputs: The inputs to validate.
    :param project_id: The ICAv2 project id to validate against.
    :param project_prefix: The ICAv2 project prefix
    """
    # Collect all data URIs from the inputs
    data_uris: List[str] = []

    # Get all fastq uris from the inputs
    for fastq_obj in inputs.get("sequenceData", {}).get("fastqListRows", []):
        # We filter out 'None' values later
        data_uris.extend([
            fastq_obj.get("read1FileUri"),
            fastq_obj.get("read2FileUri")
        ])

    # We may also have:
    # reference.tarball
    # oraReference
    # annotation
    ref_obj = inputs.get("reference", {})
    data_uris.append(ref_obj.get("tarball"))
    data_uris.append(inputs.get("oraReference"))
    data_uris.append(inputs.get("annotation"))

    # Remove empty / None values from list
    data_uris = [uri for uri in data_uris if uri]

    # Phase 1: Filemanager existence check — ALL URIs except refdata bucket
    # This confirms every input file/folder actually exists at the S3 level,
    # regardless of which bucket it's in.
    non_reference_data_uris = list(filter(
        lambda uri: not uri.startswith(f"s3://{REF_DATA_BUCKET}/"),
        data_uris
    ))
    for data_uri in non_reference_data_uris:
        # Check if it's a folder URI (ends with /)
        if data_uri.endswith("/"):
            # For folder URIs, verify at least 1 file exists under that prefix
            if not (
                    len(
                        list_files_recursively(
                            urlparse(data_uri).netloc,
                            str(Path(urlparse(data_uri).path)) + "/"
                        )
                    ) > 0
            ):
                return False, f"Folder URI '{data_uri}' has no files found under that prefix in the Filemanager"
        else:
            # For file URIs, confirm the file exists
            try:
                get_s3_object_id_from_s3_uri(data_uri)
            except S3FileNotFoundError:
                return False, f"Data URI '{data_uri}' cannot be found by the Filemanager, are you sure it exists?"

    # Phase 2: ICA project context validation
    # Only URIs outside ref/test/project-prefix need ICA project linking confirmed
    uris_to_validate = [
        uri for uri in data_uris
        if not (
            uri.startswith(f"s3://{REF_DATA_BUCKET}/") or
            uri.startswith(f"s3://{TEST_BUCKET}/") or
            uri.startswith(project_prefix)
        )
    ]

    # Validate each URI is accessible in the project context
    for data_uri in uris_to_validate:
        # Try get the icav2 object by uri
        try:
            project_data_obj = coerce_data_id_or_uri_to_project_data_obj(
                data_id_or_uri=data_uri,
            )
        except ValueError as e:
            return False, f"Data URI '{data_uri}' cannot be found in the project context '{project_id}'"

        # Then try get it in this context
        try:
            get_project_data_obj_by_id(
                project_id=project_id,
                data_id=project_data_obj.data.id
            )
        except ApiException as e:
            return False, f"Data URI '{data_uri}' cannot be found in the project context '{project_id}'"

    return True, ""


def handler(event, context) -> Dict[str, bool]:
    """
    Given a draft schema, validate it against the current schema and print the results.

    Input:
      {
        "workflowRunId": "wfr.xxx",
        "executionArn": "arn:aws:states:...",
        "data": {
          "engineParameters": {
            "projectId": "...",
            "pipelineId": "...",
            "outputUri": "s3://...",
            "logsUri": "s3://..."
          },
          "inputs": { ... },
          "tags": { ... }
        }
      }

    Output:
      {"isValid": true}   — all checks pass
      {"isValid": false}  — at least one check failed (comment written)
    """
    # Set ICAv2 env vars
    set_icav2_env_vars()

    # Get the event data
    payload_data = event.get('data')
    workflow_run_id = event.get("workflowRunId", "")
    execution_arn = event.get("executionArn", "")

    # Get the ICAv2 project id from the event
    engine_parameters = payload_data.get("engineParameters", {})

    # Get the project prefix
    project_prefix = cast(str, get_s3_key_prefix_by_project_id(engine_parameters.get("projectId")))

    # Confirm the engine parameters match
    is_valid, comment = validate_engine_parameters(
        engine_parameters,
        workflow_run_id=workflow_run_id,
        project_prefix=project_prefix,
    )

    # Check if the inputs are also valid
    if is_valid:
        # Get the inputs and confirm that the data uris are valid
        # and are accessible in the right project context
        inputs = payload_data.get("inputs")
        # Validate the inputs
        is_valid, comment = validate_inputs(
            inputs,
            project_id=engine_parameters.get("projectId"),
            project_prefix=project_prefix
        )

    # Somewhere along the way, the validation failed
    if not is_valid:
        add_comment_to_workflow_run(
            workflow_run_orcabus_id=workflow_run_id,
            comment=_format_comment_with_arn(
                f"Post schema validation failed: {comment}",
                execution_arn
            ),
            author=COMMENT_AUTHOR
        )
        return {
            "isValid": False
        }

    return {
        "isValid": True
    }
