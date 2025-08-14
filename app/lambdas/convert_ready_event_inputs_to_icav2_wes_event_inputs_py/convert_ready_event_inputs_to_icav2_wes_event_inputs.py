#!/usr/bin/env python3

"""
BCLConvert InteropQC ready to ICAv2 WES request

Given a BCLConvert InteropQC ready event object, convert this to an ICAv2 WES request event detail

Inputs are as follows:

{
  // Data inputs
  "sampleName": "L2301197",
  "sequenceData": {
    "fastqListRows": [
      {
        "rgid": "L2301197",
        "rglb": "L2301197",
        "rgsm": "L2301197",
        "lane": 1,
        "read1FileUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R1_001.fastq.ora",
        "read2FileUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R2_001.fastq.ora"
      }
    ]
  },
  // Reference inputs
  "reference": {
    "name": "hg38",
    "structure": "linear",
    "tarball": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/dragen-hash-tables/v11-r5/chm13_v2-cnv-graph-hla-methyl_cg-rna/chm13_v2-cnv.graph.hla.methyl_cg.rna-11-r5.0-1.tar.gz"
  },
  "annotationFile": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/gencode/hg38/v39/gencode.v39.annotation.gtf",
  "oraReference": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/dragen-ora/v2/ora_reference_v2.tar.gz",
  "alignmentOptions": {},
  "snvVariantCallerOptions": {
    "enableVcfCompression": true,
    "enableVcfIndexing": true
  },
  "geneFusionDetectionOptions": {
    "enableRnaGeneFusion": true
  },
  "geneExpressionQuantificationOptions": {
    "enableRnaQuantification": true
  },
  "spliceVariantCallerOptions": {
    "enableRnaSpliceVariant": true
  },
  "mafConversionOptions": {},
  "nirvanaAnnotationOptions": {}
}
With the outputs as follows:

{
  "alignment_options": {
    "enable_duplicate_marking": true
  },
  "reference": {
    "name": "hg38",
    "structure": "linear",
    "tarball": {
      "class": "File",
      "location": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/dragen-hash-tables/v11-r5/chm13_v2-cnv-graph-hla-methyl_cg-rna/chm13_v2-cnv.graph.hla.methyl_cg.rna-11-r5.0-1.tar.gz"
    }
  },
  "annotation_file": {
    "class": "File",
    "location": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/gencode/hg38/v39/gencode.v39.annotation.gtf"
  },
  "ora_reference": {
    "class": "File",
    "location": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/dragen-ora/v2/ora_reference_v2.tar.gz"
  },
  "sample_name": "L2301197",
  "sequence_data": {
    "fastq_list_rows": [
      {
        "rgid": "L2301197",
        "rglb": "L2301197",
        "rgsm": "L2301197",
        "lane": 1,
        "read_1": {
          "class": "File",
          "location": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R1_001.fastq.ora"
        },
        "read_2": {
          "class": "File",
          "location": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R2_001.fastq.ora"
        }
      }
    ]
  },
  "snv_variant_caller_options": {
    "enable_vcf_compression": true,
    "enable_vcf_indexing": true
  },
  "gene_fusion_detection_options": {
    "enable_rna_gene_fusion": true
  },
  "gene_expression_quantification_options": {
    "enable_rna_quantification": true
  },
  "splice_variant_caller_options": {
    "enable_rna_splice_variant": true
  }
}

"""

from typing import Dict, Any, Union, List


def to_snake_case(s: str) -> str:
    """
    Convert a string to snake_case.
    :param s: The input string.
    :return: The snake_case version of the input string.
    """
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def recursive_snake_case(d: Union[Dict[str, Any] | List[Any] | str]) -> Any:
    """
    Convert all keys in a dictionary to snake_case recursively.
    If the value is a list, we also need to convert each item in the list if it is a dictionary.
    :param d:
    :return:
    """
    if not isinstance(d, dict) and not isinstance(d, list):
        return d

    if isinstance(d, dict):
        return {to_snake_case(k): recursive_snake_case(v) for k, v in d.items()}

    return [recursive_snake_case(item) for item in d]


def update_fqlr_input_name(input_name: str) -> str:
    if input_name == 'read1FileUri':
        return 'read_1'
    if input_name == 'read2FileUri':
        return 'read_2'
    return input_name


def cwlify_file(file_uri: str) -> Dict[str, str]:
    return {
        "class": "File",
        "location": file_uri
    }


def handler(event, context) -> Dict[str, Any]:
    """
    Convert the BCLConvert InteropQC ready event to an ICAv2 WES request event detail.
    :param event:
    :param context:
    :return:
    """
    inputs = event['inputs']

    # If sequenceData contains either fastqListRows or tumorFastqListRows, we need to edit to CWL file types
    for sequence_data_key_iter_ in ['sequenceData']:
        if 'fastqListRows' not in inputs.get(sequence_data_key_iter_, {}):
            continue
        inputs[sequence_data_key_iter_]['fastqListRows'] = list(map(
            lambda fqlr_iter_: dict(map(
                lambda fqlr_item: (
                    (update_fqlr_input_name(fqlr_item[0]), cwlify_file(fqlr_item[1]))
                    if not update_fqlr_input_name(fqlr_item[0]) == fqlr_item[0]
                    else
                    (fqlr_item[0], fqlr_item[1])  # Keep the original key if it is not read1FileUri or read2FileUri
                ),
                fqlr_iter_.items()
            )),
            inputs[sequence_data_key_iter_]['fastqListRows']
        ))

    # Update references
    inputs['reference']['tarball'] = cwlify_file(inputs['reference']['tarball'])
    if 'oraReference' in inputs:
        inputs['oraReference'] = cwlify_file(inputs['oraReference'])
    if 'annotationFile' in inputs:
        inputs['annotationFile'] = cwlify_file(inputs['annotationFile'])

    return {
        "inputs": recursive_snake_case(inputs)
    }


# if __name__ == "__main__":
#     import json
#
#     print(
#         json.dumps(
#             handler(
#                 event={
#                     "dragenWgtsDnaReadyEventDetail": {
#                         "portalRunId": "20250606efgh1234",
#                         "timestamp": "2025-06-06T04:39:31+00:00",
#                         "status": "READY",
#                         "workflowName": "dragen-wgts-dna",
#                         "workflowVersion": "4.4.4",
#                         "workflowRunName": "umccr--automated--dragen-wgts-dna--4-4-4--20250606efgh1234",
#                         "linkedLibraries": [
#                             {
#                                 "libraryId": "L2301197",
#                                 "orcabusId": "lib.01JBMVHM2D5GCC7FTC20K4FDFK"
#                             }
#                         ],
#                         "payload": {
#                             "refId": "4d8b4468-55da-490f-8aab-0adcaed3fc33",
#                             "version": "2025.06.06",
#                             "data": {
#                                 "inputs": {
#                                     "alignmentOptions": {
#                                         "enableDuplicateMarking": True
#                                     },
#                                     "reference": {
#                                         "name": "hg38",
#                                         "structure": "graph",
#                                         "tarball": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/dragen-hash-tables/v11-r5/hg38-alt_masked-cnv-graph-hla-methyl_cg-rna/hg38-alt_masked.cnv.graph.hla.methyl_cg.rna-11-r5.0-1.tar.gz"
#                                     },
#                                     "oraReference": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/dragen-ora/v2/ora_reference_v2.tar.gz",
#                                     "sampleName": "L2301197",
#                                     "targetedCallerOptions": {
#                                         "enableTargeted": [
#                                             "cyp2d6"
#                                         ]
#                                     },
#                                     "sequenceData": {
#                                         "fastqListRows": [
#                                             {
#                                                 "rgid": "L2301197",
#                                                 "rglb": "L2301197",
#                                                 "rgsm": "L2301197",
#                                                 "lane": 1,
#                                                 "read1FileUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R1_001.fastq.ora",
#                                                 "read2FileUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R2_001.fastq.ora"
#                                             }
#                                         ]
#                                     },
#                                     "snv_variant_caller_options": {
#                                         "enableVcfCompression": True,
#                                         "enableVcfIndexing": True,
#                                         "qcDetectContamination": True,
#                                         "vcMnvEmitComponentCalls": True,
#                                         "vcCombinePhasedVariantsDistance": 2,
#                                         "vcCombinePhasedVariantsDistanceSnvsOnly": 2
#                                     }
#                                 },
#                                 "engineParameters": {
#                                     "pipelineId": "5009335a-8425-48a8-83c4-17c54607b44a",
#                                     "projectId": "ea19a3f5-ec7c-4940-a474-c31cd91dbad4",
#                                     "outputUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/analysis/dragen-wgts-dna/20250606efgh1234/",
#                                     "logsUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/logs/dragen-wgts-dna/20250606efgh1234/"
#                                 },
#                                 "tags": {
#                                     "libraryId": "L2301197"
#                                 }
#                             }
#                         }
#                     },
#                     "defaultPipelineId": "5009335a-8425-48a8-83c4-17c54607b44a",
#                     "defaultProjectId": "ea19a3f5-ec7c-4940-a474-c31cd91dbad4"
#                 },
#                 context=None
#             ),
#             indent=4
#         )
#     )
#
#     # {
#     #     "icav2WesRequestEventDetail": {
#     #         "name": "umccr--automated--dragen-wgts-dna--4-4-4--20250606efgh1234",
#     #         "inputs": {
#     #             "alignment_options": {
#     #                 "enable_duplicate_marking": true
#     #             },
#     #             "reference": {
#     #                 "name": "hg38",
#     #                 "structure": "graph",
#     #                 "tarball": {
#     #                     "class": "File",
#     #                     "location": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/dragen-hash-tables/v11-r5/hg38-alt_masked-cnv-graph-hla-methyl_cg-rna/hg38-alt_masked.cnv.graph.hla.methyl_cg.rna-11-r5.0-1.tar.gz"
#     #                 }
#     #             },
#     #             "ora_reference": {
#     #                 "class": "File",
#     #                 "location": "s3://pipeline-prod-cache-503977275616-ap-southeast-2/byob-icav2/reference-data/dragen-ora/v2/ora_reference_v2.tar.gz"
#     #             },
#     #             "sample_name": "L2301197",
#     #             "targeted_caller_options": {
#     #                 "enable_targeted": [
#     #                     "cyp2d6"
#     #                 ]
#     #             },
#     #             "sequence_data": {
#     #                 "fastq_list_rows": [
#     #                     {
#     #                         "rgid": "L2301197",
#     #                         "rglb": "L2301197",
#     #                         "rgsm": "L2301197",
#     #                         "lane": 1,
#     #                         "read_1": {
#     #                             "class": "File",
#     #                             "location": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R1_001.fastq.ora"
#     #                         },
#     #                         "read_2": {
#     #                             "class": "File",
#     #                             "location": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/test_data/ora-testing/input_data/MDX230428_L2301197_S7_L004_R2_001.fastq.ora"
#     #                         }
#     #                     }
#     #                 ]
#     #             },
#     #             "snv_variant_caller_options": {
#     #                 "enable_vcf_compression": true,
#     #                 "enable_vcf_indexing": true,
#     #                 "qc_detect_contamination": true,
#     #                 "vc_mnv_emit_component_calls": true,
#     #                 "vc_combine_phased_variants_distance": 2,
#     #                 "vc_combine_phased_variants_distance_snvs_only": 2
#     #             }
#     #         },
#     #         "engineParameters": {
#     #             "outputUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/analysis/dragen-wgts-dna/20250606efgh1234/",
#     #             "logsUri": "s3://pipeline-dev-cache-503977275616-ap-southeast-2/byob-icav2/development/logs/dragen-wgts-dna/20250606efgh1234/",
#     #             "projectId": "ea19a3f5-ec7c-4940-a474-c31cd91dbad4",
#     #             "pipelineId": "5009335a-8425-48a8-83c4-17c54607b44a"
#     #         },
#     #         "tags": {
#     #             "libraryId": "L2301197",
#     #             "portalRunId": "20250606efgh1234"
#     #         }
#     #     }
#     # }
