import { PythonUvFunction } from '@orcabus/platform-cdk-constructs/lambda';

/**
 * Lambda function interface.
 */
export type LambdaNameList =
  // Draft Data lambdas
  | 'checkNtsmInternal'
  | 'getFastqIdListFromRgidList'
  | 'getFastqListRowsFromRgidList'
  | 'getFastqRgidsFromLibraryId'
  | 'getLibraries'
  | 'getMetadataTags'
  | 'getQcSummaryStatsFromRgidList'
  // Payload comparison and WRU generation
  | 'comparePayload'
  | 'generateWruEventObjectWithMergedData'
  | 'getMissingSchemaFields'
  // Validation lambdas
  | 'validateDraftCompleteSchema'
  | 'postSchemaValidation'
  // Commentary Functions
  | 'addPopulateDraftComment'
  // Ready to ICAv2 WES lambdas
  | 'convertReadyEventInputsToIcav2WesEventInputs'
  // ICAv2 WES to WRSC Event lambdas
  | 'convertIcav2WesEventToWruEvent'
  | 'addWesFailureComment';

export const lambdaNameList: LambdaNameList[] = [
  // Draft Data lambdas
  'checkNtsmInternal',
  'getFastqIdListFromRgidList',
  'getFastqListRowsFromRgidList',
  'getFastqRgidsFromLibraryId',
  'getLibraries',
  'getMetadataTags',
  'getQcSummaryStatsFromRgidList',
  // Payload comparison and WRU generation
  'comparePayload',
  'generateWruEventObjectWithMergedData',
  'getMissingSchemaFields',
  // Validation lambdas
  'validateDraftCompleteSchema',
  'postSchemaValidation',
  // Commentary Functions
  'addPopulateDraftComment',
  // Ready to ICAv2 WES lambdas
  'convertReadyEventInputsToIcav2WesEventInputs',
  // ICAv2 WES to WRSC Event lambdas
  'convertIcav2WesEventToWruEvent',
  'addWesFailureComment',
];

// Requirements interface for Lambda functions
export interface LambdaRequirements {
  needsOrcabusApiTools?: boolean;
  needsIcav2Tools?: boolean;
  needsHigherMemory?: boolean;
  needsSsmParametersAccess?: boolean;
  needsSchemaRegistryAccess?: boolean;
  needsExternalBucketInfo?: boolean;
  needsWorkflowInfo?: boolean;
  needsRepoUrl?: boolean;
}

// Lambda requirements mapping
export const lambdaRequirementsMap: Record<LambdaNameList, LambdaRequirements> = {
  // Draft Data lambdas
  checkNtsmInternal: {
    needsOrcabusApiTools: true,
  },
  getFastqIdListFromRgidList: {
    needsOrcabusApiTools: true,
  },
  getFastqListRowsFromRgidList: {
    needsOrcabusApiTools: true,
    needsExternalBucketInfo: true,
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
  // Payload comparison and WRU generation
  comparePayload: {},
  generateWruEventObjectWithMergedData: { needsOrcabusApiTools: true },
  getMissingSchemaFields: { needsSchemaRegistryAccess: true, needsSsmParametersAccess: true },
  // Validation lambdas
  validateDraftCompleteSchema: {
    needsSchemaRegistryAccess: true,
    needsSsmParametersAccess: true,
    needsOrcabusApiTools: true,
    needsWorkflowInfo: true,
  },
  postSchemaValidation: {
    needsOrcabusApiTools: true,
    needsIcav2Tools: true,
    needsExternalBucketInfo: true,
    needsWorkflowInfo: true,
  },
  // Commentary Functions
  addPopulateDraftComment: {
    needsOrcabusApiTools: true,
    needsWorkflowInfo: true,
    needsRepoUrl: true,
  },
  // Ready to ICAv2 WES lambdas - no requirements
  convertReadyEventInputsToIcav2WesEventInputs: {},
  // ICAv2 WES to WRSC Event lambdas
  convertIcav2WesEventToWruEvent: {
    needsOrcabusApiTools: true,
  },
  addWesFailureComment: {
    needsOrcabusApiTools: true,
    needsWorkflowInfo: true,
  },
};

export interface LambdaInput {
  lambdaName: LambdaNameList;
}

export interface LambdaObject extends LambdaInput {
  lambdaFunction: PythonUvFunction;
}
