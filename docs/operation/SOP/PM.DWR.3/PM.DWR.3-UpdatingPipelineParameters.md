# PM.DWR.3 — Updating Pipeline Parameters

## Purpose

Update SSM parameters that control the Dragen WGTS RNA pipeline behaviour (default references, input overrides, project IDs, etc.).

## Prerequisites

- AWS CLI configured with access to SSM Parameter Store
- Understanding of which parameter needs changing and why

## Parameter Locations

All parameters live under the SSM prefix: `/orcabus/workflows/dragen-wgts-rna/`

| Parameter | Description |
|---|---|
| `workflow-version` | Current default workflow version |
| `payload-version` | Current payload schema version |
| `icav2-project-id` | Default ICAv2 project for the environment |
| `logs-prefix` | S3 prefix for analysis logs |
| `output-prefix` | S3 prefix for analysis outputs |
| `pipeline-ids-by-workflow-version/<version>` | ICAv2 pipeline ID per version |
| `inputs-by-workflow-version/<version>` | Default input overrides per version |
| `reference-by-workflow-version/<version>` | Default reference path per version |

## Procedure

### 1. Identify the parameter to change

Check `infrastructure/stage/constants.ts` for the full list of SSM parameter paths used by this service.

### 2. Update via AWS CLI

```bash
aws ssm put-parameter \
  --name "/orcabus/workflows/dragen-wgts-rna/<PARAMETER_NAME>" \
  --value "<NEW_VALUE>" \
  --type String \
  --overwrite
```

### 3. Verify

Submit a test DRAFT event and verify the populated payload reflects the new parameter value.

## Notes

- SSM parameter changes take effect immediately for new executions
- In-flight executions use the value that was read at the time of their execution
- If the parameter is also defined in CDK constants, update both to stay in sync for future deployments
