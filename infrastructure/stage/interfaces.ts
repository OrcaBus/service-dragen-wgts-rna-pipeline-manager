/*

Interfaces for the application

 */

import { SsmParameterPaths, SsmParameterValues } from './ssm/interfaces';

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

  // Workflow manager stuff
  isNewWorkflowManagerDeployed: boolean;
}

/* Set versions */
export type WorkflowVersionType = '4.4.4';
export type OraReferenceVersionType = '2.7.0';
export type AnnotationVersionType = '44';

export interface Reference {
  name: string;
  structure: string;
  tarball: string;
}
