# PM.DWR.5 — Troubleshooting

## Purpose

Guide for diagnosing and resolving common issues with the Dragen WGTS RNA Pipeline Manager.

## Common Issues

### 1. Populate Draft Data fails

**Symptoms**: The `populateDraftData` state machine fails at a Lambda invocation step.

**Diagnosis**:
1. Open the failed execution in the Step Functions console
2. Identify which Lambda failed and check its CloudWatch Logs
3. Common causes:
   - Fastq Glue cannot find FASTQ files for the library
   - Metadata service returns no results for the library
   - SSM parameter is missing or has an unexpected value

**Resolution**:
- Verify the library exists in the metadata service
- Check that FASTQ data has been ingested for the library's RGID list
- Verify SSM parameters exist under `/orcabus/workflows/dragen-wgts-rna/`
- If data is still being ingested, the state machine will wait on a task token — no action needed

### 2. Schema validation fails

**Symptoms**: A comment is written to the workflow run record saying validation failed. The pipeline does not progress to READY.

**Diagnosis**:
1. Read the comment on the workflow run record in Workflow Manager
2. Compare the populated payload against the [complete-data draft schema](../../../app/event-schemas/complete-data-draft/)

**Resolution**:
- Identify the missing or invalid field
- If a required field was not populated, check the populate state machine for errors
- If the schema itself needs updating, follow [PM.DWR.2](../PM.DWR.2/PM.DWR.2-NewDragenWgtsRnaPipelineDeployment.md)

### 3. ICAv2 analysis fails

**Symptoms**: The `WorkflowRunUpdate` event shows status FAILED.

**Diagnosis**:
1. Check the failure comment written by `add_wes_failure_comment` Lambda
2. Look at the ICAv2 analysis logs (accessible via the `logsUri` in the payload)
3. Common causes:
   - Invalid input file paths
   - Reference file not accessible from the ICAv2 project
   - Pipeline version incompatibility

**Resolution**:
- Fix the underlying input/reference issue
- Resubmit the DRAFT event (follow PM.DWR.1)

### 4. Downstream services don't receive SUCCEEDED event

**Symptoms**: Oncoanalyser WGTS RNA, Arriba, or RNAsum don't trigger after a successful run.

**Diagnosis**:
1. Verify the `WorkflowRunUpdate` SUCCEEDED event was emitted (check EventBridge)
2. Check that downstream services' event rules are correctly configured
3. Check downstream services' Step Functions for any failed executions

**Resolution**:
- If the event was emitted but not consumed, check the downstream event rule patterns
- If the downstream state machine failed, troubleshoot in that service

### 5. Step Function execution stuck / waiting

**Symptoms**: The populate state machine is in a `RUNNING` state for an extended period.

**Diagnosis**:
1. Check which step is currently active — likely waiting on a task token
2. Task token waits are typically for FASTQ data to become available

**Resolution**:
- This is normal if FASTQ data is still being processed (e.g. sequencing run in progress)
- If the wait is unexpected, check Fastq Glue for the status of the FASTQ files
- A state machine can be redriven from the Step Functions console if a Lambda bug was fixed

## Useful Commands

```bash
# Check SSM parameters
aws ssm get-parameters-by-path \
  --path "/orcabus/workflows/dragen-wgts-rna/" \
  --recursive

# List recent Step Function executions
aws stepfunctions list-executions \
  --state-machine-arn "<state-machine-arn>" \
  --status-filter FAILED \
  --max-results 10
```

## Escalation

If the issue cannot be resolved using this guide:
1. Check the service's CloudWatch dashboards
2. Review recent deployments for breaking changes
3. Escalate to the platform team with the execution ARN and error details
