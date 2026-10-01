nextflow.enable.dsl=2
include { UMITOOLS_EXTRACT } from '../../modules/local/umitools'
workflow {
    UMITOOLS_EXTRACT(Channel.of(tuple('sample', file(params.test_pattern_file))))
}
