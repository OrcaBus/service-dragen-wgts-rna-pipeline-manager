/*

Interfaces for the application

 */

import { SsmParameterPaths, SsmParameterValues } from './ssm/interfaces';
import { StageName } from '@orcabus/platform-cdk-constructs/shared-config/accounts';

/**
 * Stateful application stack interface.
 */

export interface StatefulApplicationStackConfig {
  // Values
  // Detail
  ssmParameterValues: SsmParameterValues;

  // Keys
  ssmParameterPaths: SsmParameterPaths;
}

/**
 * Stateless application stack interface.
 */
export interface StatelessApplicationStackConfig {
  // Event Stuff
  eventBusName: string;

  // SSM Parameter stuff
  ssmParameterPaths: SsmParameterPaths;

  // Stage Name
  stageName: StageName;

  // Pipeline cache bucket
  pipelineCacheBucketName: string;
  pipelineCachePrefix: string;
}

/* Set versions */
export type WorkflowVersionType = '4.4.4';
export type PayloadVersionType = '2025.08.05';
export type OraReferenceVersionType = '2.7.0';
export type AnnotationVersionType = '44';

/* Consts of types */
export const payloadVersionList: PayloadVersionType[] = ['2025.08.05'];

export interface Reference {
  name: string;
  structure: string;
  tarball: string;
}
