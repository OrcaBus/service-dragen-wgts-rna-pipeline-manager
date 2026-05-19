import { PythonUvFunction } from '@orcabus/platform-cdk-constructs/lambda';

export type LambdaName =
  // Draft Data lambdas
  | 'checkNtsmInternal'
  | 'getFastqIdListFromRgidList'
  | 'getFastqListRowsFromRgidList'
  | 'getFastqRgidsFromLibraryId'
  | 'getLibraries'
  | 'getMetadataTags'
  | 'getQcSummaryStatsFromRgidList'
  // Validation lambda
  | 'validateDraftCompleteSchema'
  | 'postSchemaValidation'
  // Ready to ICAv2 WES lambdas
  | 'convertReadyEventInputsToIcav2WesEventInputs'
  // ICAv2 WES to WRSC Event lambdas
  | 'convertIcav2WesEventToWruEvent';

export const lambdaNameList: LambdaName[] = [
  // Draft Data lambdas
  'checkNtsmInternal',
  'getFastqIdListFromRgidList',
  'getFastqListRowsFromRgidList',
  'getFastqRgidsFromLibraryId',
  'getLibraries',
  'getMetadataTags',
  'getQcSummaryStatsFromRgidList',
  // Validation lambda
  'validateDraftCompleteSchema',
  'postSchemaValidation',
  // Ready to ICAv2 WES lambdas
  'convertReadyEventInputsToIcav2WesEventInputs',
  // ICAv2 WES to WRSC Event lambdas
  'convertIcav2WesEventToWruEvent',
];

// Requirements interface for Lambda functions
export interface LambdaRequirements {
  needsOrcabusApiTools?: boolean;
  needsIcav2Tools?: boolean;
  needsSchemaRegistryAccess?: boolean;
  needsSsmParametersAccess?: boolean;
  needsHigherMemory?: boolean;
  needsBucketEnvVars?: boolean;
  needsWorkflowEnvVars?: boolean;
}

// Lambda requirements mapping
export const lambdaRequirementsMap: Record<LambdaName, LambdaRequirements> = {
  // Draft Data lambdas
  checkNtsmInternal: {
    needsOrcabusApiTools: true,
  },
  getFastqIdListFromRgidList: {
    needsOrcabusApiTools: true,
  },
  getFastqListRowsFromRgidList: {
    needsOrcabusApiTools: true,
  },
  getFastqRgidsFromLibraryId: {
    needsOrcabusApiTools: true,
  },
  getLibraries: {
    needsOrcabusApiTools: true,
  },
  getMetadataTags: {
    needsOrcabusApiTools: true,
  },
  getQcSummaryStatsFromRgidList: {
    needsOrcabusApiTools: true,
  },
  validateDraftCompleteSchema: {
    needsOrcabusApiTools: true,
    needsSchemaRegistryAccess: true,
    needsSsmParametersAccess: true,
  },
  postSchemaValidation: {
    needsOrcabusApiTools: true,
    needsIcav2Tools: true,
    needsHigherMemory: true,
    needsBucketEnvVars: true,
    needsWorkflowEnvVars: true,
  },
  // Convert ready to ICAv2 WES Event - no requirements
  convertReadyEventInputsToIcav2WesEventInputs: {},
  // Needs OrcaBus toolkit to get the wrsc event
  convertIcav2WesEventToWruEvent: {
    needsOrcabusApiTools: true,
  },
};

export interface BuildAllLambdaProps {
  refDataBucketName: string;
  testDataBucketName: string;
}

export interface LambdaInput extends BuildAllLambdaProps {
  lambdaName: LambdaName;
}

export interface LambdaObject {
  lambdaName: LambdaName;
  lambdaFunction: PythonUvFunction;
}
