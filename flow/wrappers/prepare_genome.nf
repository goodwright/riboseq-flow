include { PREPARE_RIBOSEQ_REFERENCE } from '../../subworkflows/prepare_reference.nf'

workflow {
    PREPARE_RIBOSEQ_REFERENCE (
        params.fasta,
        params.gtf,
        params.contaminants_fasta
    )
}