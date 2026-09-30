nextflow.enable.dsl=2
include { IDENTIFY_PSITES } from '../../modules/local/ribowaltz'
workflow {
    IDENTIFY_PSITES(file("${projectDir}/input.bam"), file("${projectDir}/input.gtf"),
                   file("${projectDir}/input.fasta"), file("${projectDir}/input.tsv"))
}
