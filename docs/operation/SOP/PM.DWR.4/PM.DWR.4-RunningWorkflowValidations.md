# PM.DWR.4 — Running Workflow Validations

## Purpose

Validate that the Dragen WGTS RNA pipeline runs correctly after a new version deployment or configuration change.

## Prerequisites

- A test RNA library available in the environment (beta or gamma)
- Access to submit DRAFT events and monitor Step Functions executions

## Procedure

### 1. Select test cases

Choose at least one RNA library that has been previously processed successfully to use as a validation baseline.

### 2. Submit a DRAFT event

Follow [PM.DWR.1 — Manual Pipeline Execution](../PM.DWR.1/PM.DWR.1-ManualPipelineExecution.md) to submit a DRAFT event for the test library.

### 3. Monitor the pipeline

1. **Populate stage** — Verify the `populateDraftData` state machine completes successfully
2. **Validation stage** — Verify the `validateDraftDataAndPutReadyEvent` state machine promotes to READY
3. **Submission stage** — Verify the `readyEventToIcav2WesRequestEvent` state machine emits an ICAv2 WES request
4. **ICAv2 execution** — Monitor the analysis in the ICAv2 console until completion
5. **Result reporting** — Verify the `icav2WesEventToWrscEvent` state machine emits a SUCCEEDED `WorkflowRunUpdate`

### 4. Verify outputs

- Check that the output files are written to the expected S3 location
- Compare key outputs (alignment metrics, variant calls) against the baseline run
- Verify downstream services (Oncoanalyser WGTS RNA, Arriba, RNAsum) pick up the SUCCEEDED event

### 5. Document results

Record validation results including:

- Library ID tested
- Workflow version
- Execution time
- Output comparison notes
- Pass/fail determination

## Validation Criteria

- Pipeline completes without errors
- Output file structure matches expected layout
- Key metrics are within acceptable range of baseline
