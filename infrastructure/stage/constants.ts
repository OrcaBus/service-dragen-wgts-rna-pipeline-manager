/* Directory constants */
import path from 'path';
import { StageName } from '@orcabus/platform-cdk-constructs/shared-config/accounts';
import {
  AnnotationVersionType,
  OraReferenceVersionType,
  Reference,
  WorkflowVersionType,
} from './interfaces';
import { DATA_SCHEMA_REGISTRY_NAME } from '@orcabus/platform-cdk-constructs/shared-config/event-bridge';

export const APP_ROOT = path.join(__dirname, '../../app');
export const LAMBDA_DIR = path.join(APP_ROOT, 'lambdas');
export const STEP_FUNCTIONS_DIR = path.join(APP_ROOT, 'step-functions-templates');
export const EVENT_SCHEMAS_DIR = path.join(APP_ROOT, 'event-schemas');

/* Workflow constants */
export const WORKFLOW_NAME = 'dragen-wgts-rna';

// Yet to implement draft events into this service
// However, because this workflow has the same workflow name as the
// existing production workflow, we need to filter on the payload version
// to prevent the wrong service from being triggered
export const DEFAULT_WORKFLOW_VERSION: WorkflowVersionType = '4.4.4';
export const DEFAULT_PAYLOAD_VERSION = '2025.08.05';

// Yet to implement draft events into this service
export const WORKFLOW_LOGS_PREFIX = `s3://{__CACHE_BUCKET__}/{__CACHE_PREFIX__}logs/${WORKFLOW_NAME}/`;
export const WORKFLOW_OUTPUT_PREFIX = `s3://{__CACHE_BUCKET__}/{__CACHE_PREFIX__}analysis/${WORKFLOW_NAME}/`;

/* We extend this every time we release a new version of the workflow */
/* This is added into our SSM Parameter Store to allow us to map workflow versions to pipeline IDs */
export const WORKFLOW_VERSION_TO_DEFAULT_ICAV2_PIPELINE_ID_MAP: Record<
  WorkflowVersionType,
  string
> = {
  // https://github.com/umccr/cwl-ica/releases/tag/dragen-wgts-rna-pipeline%2F4.4.4__20251005025030
  '4.4.4': '079d5aa9-664c-472d-9baf-1e6a6c542401',
};

export const WORKFLOW_VERSION_TO_DEFAULT_REFERENCE_PATHS_MAP: Record<
  WorkflowVersionType,
  Reference
> = {
  '4.4.4': {
    name: 'hg38',
    structure: 'linear',
    tarball:
      's3://reference-data-503977275616-ap-southeast-2/refdata/dragen-hash-tables/v11-r5/hg38-alt_masked-cnv-hla-methyl_cg-methylated_combined/hg38-alt_masked.cnv.hla.methyl_cg.methylated_combined.rna-11-r5.0-1.tar.gz',
  },
};

export const ORA_VERSION_TO_DEFAULT_ORA_REFERENCE_PATHS_MAP: Record<
  OraReferenceVersionType,
  string
> = {
  '2.7.0':
    's3://reference-data-503977275616-ap-southeast-2/refdata/dragen-ora/v2/ora_reference_v2.tar.gz',
};

export const DEFAULT_ORA_VERSION: OraReferenceVersionType = '2.7.0';

export const ANNOTATION_VERSION_TO_ANNOTATION_PATHS_MAP: Record<AnnotationVersionType, string> = {
  '44': 's3://reference-data-503977275616-ap-southeast-2/refdata/gencode/hg38/v44/gencode.v44.annotation.gtf.gz',
};

export const WORKFLOW_VERSION_TO_DEFAULT_ANNOTATION_PATHS_MAP: Record<
  WorkflowVersionType,
  AnnotationVersionType
> = {
  '4.4.4': '44',
};

export const DEFAULT_WORKFLOW_INPUTS_BY_VERSION_MAP: Record<WorkflowVersionType, object> = {
  '4.4.4': {
    alignmentOptions: {
      rrnaFilterEnable: true,
    },
    snvVariantCallerOptions: {
      enableVcfCompression: true,
      enableVcfIndexing: true,
    },
    geneFusionDetectionOptions: {
      enableRnaGeneFusion: true,
    },
    geneExpressionQuantificationOptions: {
      enableRnaQuantification: true,
    },
    spliceVariantCallerOptions: {
      enableRnaSpliceVariant: true,
    },
  },
};

/* SSM Parameter Paths */
export const SSM_PARAMETER_PATH_PREFIX = path.join(`/orcabus/workflows/${WORKFLOW_NAME}/`);
// Workflow Parameters
export const SSM_PARAMETER_PATH_WORKFLOW_NAME = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'workflow-name'
);
export const SSM_PARAMETER_PATH_DEFAULT_WORKFLOW_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'default-workflow-version'
);
// Input parameters
export const SSM_PARAMETER_PATH_PREFIX_INPUTS_BY_WORKFLOW_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'inputs-by-workflow-version'
);
// Engine Parameters
export const SSM_PARAMETER_PATH_PREFIX_PIPELINE_IDS_BY_WORKFLOW_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'pipeline-ids-by-workflow-version'
);
export const SSM_PARAMETER_PATH_ICAV2_PROJECT_ID = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'icav2-project-id'
);
export const SSM_PARAMETER_PATH_PAYLOAD_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'payload-version'
);
export const SSM_PARAMETER_PATH_LOGS_PREFIX = path.join(SSM_PARAMETER_PATH_PREFIX, 'logs-prefix');
export const SSM_PARAMETER_PATH_OUTPUT_PREFIX = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'output-prefix'
);

// Reference Parameters
export const SSM_PARAMETER_PATH_PREFIX_REFERENCE_PATHS_BY_WORKFLOW_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'default-reference-paths-by-workflow-version'
);
export const SSM_PARAMETER_PATH_PREFIX_ORA_REFERENCE_PATHS_BY_WORKFLOW_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'ora-reference-paths-by-ora-version'
);
export const SSM_PARAMETER_PATH_PREFIX_ANNOTATION_VERSIONS_BY_WORKFLOW_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'annotation-versions-by-workflow-version'
);
export const SSM_PARAMETER_PATH_PREFIX_ANNOTATION_REFERENCE_PATHS_BY_ANNOTATION_VERSION = path.join(
  SSM_PARAMETER_PATH_PREFIX,
  'annotation-paths-by-annotation-version'
);

/* Event Constants */
export const EVENT_BUS_NAME = 'OrcaBusMain';
export const EVENT_SOURCE = 'orcabus.dragenwgtsrna';
export const WORKFLOW_RUN_STATE_CHANGE_DETAIL_TYPE = 'WorkflowRunStateChange';
export const WORKFLOW_RUN_UPDATE_DETAIL_TYPE = 'WorkflowRunUpdate';
export const ICAV2_WES_REQUEST_DETAIL_TYPE = 'Icav2WesRequest';
export const ICAV2_WES_STATE_CHANGE_DETAIL_TYPE = 'Icav2WesAnalysisStateChange';

export const WORKFLOW_MANAGER_EVENT_SOURCE = 'orcabus.workflowmanager';
export const ICAV2_WES_EVENT_SOURCE = 'orcabus.icav2wesmanager';

// Yet to implement draft events into this service
export const FASTQ_SYNC_DETAIL_TYPE = 'FastqSync';

/* Event rule constants */
// Yet to implement draft events into this service
export const DRAFT_STATUS = 'DRAFT';
export const READY_STATUS = 'READY';

/* Schema constants */
// Yet to implement draft events into this service
export const SCHEMA_REGISTRY_NAME = DATA_SCHEMA_REGISTRY_NAME;
export const SSM_SCHEMA_ROOT = path.join(SSM_PARAMETER_PATH_PREFIX, 'schemas');

/* Future proofing */
export const NEW_WORKFLOW_MANAGER_IS_DEPLOYED: Record<StageName, boolean> = {
  BETA: true,
  GAMMA: false,
  PROD: false,
};

// Used to group event rules and step functions
export const STACK_PREFIX = 'orca-dragen-wgts-rna';
