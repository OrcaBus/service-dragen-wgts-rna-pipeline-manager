# PM.DWR.2 — Deploying a New Pipeline Version

## Purpose

Install and deploy a new version of the Dragen WGTS RNA CWL pipeline to ICAv2, and update the pipeline manager to use it.

## Prerequisites

- Access to ICAv2 with project admin permissions
- AWS CLI configured with access to SSM Parameter Store
- The new CWL workflow definition (`.cwl` file or release tag)

## Procedure

### 1. Register the CWL pipeline on ICAv2

1. Upload the new CWL workflow to ICAv2 via the CLI or web console
2. Note the new **pipeline ID** assigned by ICAv2

### 2. Update SSM parameters

Add the new pipeline ID mapping:

```bash
aws ssm put-parameter \
  --name "/orcabus/workflows/dragen-wgts-rna/pipeline-ids-by-workflow-version/<NEW_VERSION>" \
  --value "<NEW_PIPELINE_ID>" \
  --type String \
  --overwrite
```

Update the default workflow version if this becomes the new default:

```bash
aws ssm put-parameter \
  --name "/orcabus/workflows/dragen-wgts-rna/workflow-version" \
  --value "<NEW_VERSION>" \
  --type String \
  --overwrite
```

### 3. Update CDK constants

In `infrastructure/stage/constants.ts`:

1. Add the new version to `WORKFLOW_VERSION_TO_DEFAULT_ICAV2_PIPELINE_ID_MAP`
2. Update `WORKFLOW_VERSION` constant if this is the new default
3. Add any new reference or input defaults for the new version

### 4. Deploy

```bash
# Merge changes to main — CodePipeline handles beta/gamma deployment
# Manually promote to prod after validation
```

### 5. Validate

Follow [PM.DWR.4 — Running Workflow Validations](../PM.DWR.4/PM.DWR.4-RunningWorkflowValidations.md) to verify the new version works correctly.

## Rollback

If the new version has issues:

1. Revert the `workflow-version` SSM parameter to the previous value
2. Revert the CDK constants change and redeploy
