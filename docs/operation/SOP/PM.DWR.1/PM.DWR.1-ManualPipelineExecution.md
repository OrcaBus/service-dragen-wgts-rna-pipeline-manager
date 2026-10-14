# Manual Pipeline Execution

- Version: 2026.10.09
- Contact: Alexis Lucattini, [alexisl@unimelb.edu.au](mailto:alexisl@unimelb.edu.au)

Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Procedure](#procedure)
- [Confirmation](#confirmation)

## Introduction

This Pipeline Manager manages the execution of the DRAGEN WGTS RNA pipeline.
Here we describe the SOP for manual execution of the pipeline.

## Requirements

- Appropriate AWS permissions, this should be an operator level permissions for one of umccr-dev/stg/prod
- AWS credentials set up in the local environment
- Access to the OrcaBus Portal (i.e. a PORTAL_TOKEN set in the environment)
- Tools installed
  - [aws](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) version 2 or higher
  - [jq](https://github.com/jqlang/jq) version 1.7 or higher
  - [curl](https://curl.se/download.html) version 7.76.0 or higher
  - [semver](https://github.com/fsaintjacques/semver-tool)

## Procedure

To initiate a pipeline execution we need to generate an initial DRAFT event. For more details consult the main [README](../../../../README.md).
For convenience, we provide a shell script that generates and optionally submits an appropriate event.

- Familiarise yourself with the script and its parameters: [generate-WRU-draft.sh --help](./generate-WRU-draft.sh)
  - Especially check the settings in the `Globals` and `Workflow constants` sections
    - ensure the values are fit for your use case, e.g. for clinical samples match the accredited pipeline details
    - the default `--code-version` is empty; supply `--code-version` when running a workflow version other than the default.
  - Set the engine parameters (if necessary) and the single RNA library id in the positional argument.
- Execute the script (e.g. `bash generate-WRU-draft.sh --comment 'Manual rerun' <your_rna_library_id>`)
  - Note: AWS credentials need to be set on the environment as does your PORTAL_TOKEN (see the script for details)
  - Use the comment parameter to explain the reason for the manual run, this will be visible in the Portal and helpful for future reference.
- The script should produce the JSON output of the DRAFT event that can be inspected to double check that reflects the intended request
  - Take note of the generated `workflowRunName` or `portalRunId` and the URL to the OrcaBus Portal view of the workflow.
  - You can have the script save the output json file by using the `--save-draft-payload` method.

### Using --input-data

The populate draft data service will try to auto-populate inputs based on the information it already has.
This may have unintended consequences if there exists two upstream fastq sets and you want inputs from one specific set.
In this circumstance it is recommended to use `--input-data <json_file>` to provide an existing data object to populate.

Example input data JSON file:

```json
{
  "inputs": {
    "sequenceData": {
      "fastqListRows": [
        {
          "rgid": "ACGT.1.L2500568",
          "rgsm": "L2500568",
          "read1FileUri": "s3://path/to/specific/reads_R1.fastq.gz",
          "read2FileUri": "s3://path/to/specific/reads_R2.fastq.gz"
        }
      ]
    }
  }
}
```

Example usage with `--input-data`:

```bash
bash generate-WRU-draft.sh rna_library_id \
  --comment 'Redriving with specific inputs' \
  --input-data /path/to/input_data.json
```

## Confirmation

The OrcaBus [Portal](https://portal.umccr.org/) can be used to check whether the event resulted in a WorkflowRun DRAFT record.

- navigate to the Portal's WorkflowRun listing: https://portal.umccr.org/runs/workflow
- search for your WorkflowRun using the `workflowRunName` or `portalRunId`
- confirm that the WorkflowRun is listed and progressing as expected (check over time)
- once the WorkflowRun has `SUCCEEDED` the results should be available via the Portal's [Files](https://portal.umccr.org/files) view
  - simply filter by the `portalRunId`
