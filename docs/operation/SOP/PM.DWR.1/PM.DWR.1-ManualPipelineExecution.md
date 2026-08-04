# PM.DWR.1 — Manual Pipeline Execution

## Purpose

Manually submit a Dragen WGTS RNA DRAFT event to trigger a reanalysis for one or more RNA libraries.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Access to the `OrcaBusMain` EventBridge bus
- Knowledge of the library ID(s) to analyse

## Procedure

### 1. Identify the library

Determine the RNA library ID (e.g. `L2500568`) and its OrcaBus ID from the metadata service.

### 2. Set environment variables

```bash
EVENT_BUS_NAME="OrcaBusMain"
DETAIL_TYPE="WorkflowRunUpdate"
SOURCE="orcabus.manual"

WORKFLOW_NAME="dragen-wgts-rna"
WORKFLOW_VERSION="4.4.4"

LIBRARY_ID="L2500568"
```

### 3. Generate and submit the event

Use the script in the repository root README or construct the event manually:

```bash
aws events put-events --entries '[
  {
    "EventBusName": "OrcaBusMain",
    "DetailType": "WorkflowRunUpdate",
    "Source": "orcabus.manual",
    "Detail": "{\"status\":\"DRAFT\",\"workflowName\":\"dragen-wgts-rna\",\"workflowVersion\":\"4.4.4\",\"portalRunId\":\"<generated>\",\"linkedLibraries\":[{\"libraryId\":\"L2500568\",\"orcabusId\":\"lib.01...\"}]}"
  }
]'
```

### 4. Monitor execution

1. Check the Step Functions console for the `orca-dragen-wgts-rna--populateDraftData` execution
2. Verify the DRAFT is populated and promoted to READY
3. Confirm the ICAv2 analysis is submitted via the WES Manager

## Troubleshooting

- If the populate state machine fails, check CloudWatch Logs for the Lambda that errored
- If schema validation fails, a comment will be written to the workflow run record — check Workflow Manager
- See [PM.DWR.5 — Troubleshooting](../PM.DWR.5/PM.DWR.5-TroubleShooting.md) for common issues
