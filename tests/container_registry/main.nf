nextflow.enable.dsl=2

import nextflow.container.ContainerHandler

// No tasks or image pulls: exercise the actual Nextflow resolver against the
// repository's custom image declarations with a non-Docker-Hub default registry.
workflow {
    def handler = new ContainerHandler([engine: 'docker', registry: 'quay.io'])
    def modulesDir = new File(projectDir.toString(), '../../modules/local')
    def images = []
    modulesDir.eachFileMatch(~/.*\.nf/) { module ->
        def declarations = module.text =~ /container\s+['"]([^'"]+)['"]/
        declarations.each { match ->
            def image = match[1]
            if (image.contains('iraiosub/')) {
                assert image.startsWith('docker.io/iraiosub/'): "Unqualified image in ${module.name}: ${image}"
                assert handler.normalizeImageName(image) == image: "Registry changed for ${image}"
                images.add(image)
            }
        }
    }
    assert images.toSet() == [
        'docker.io/iraiosub/nf-riboseq:latest',
        'docker.io/iraiosub/nf-riboseq-qc:latest',
        'docker.io/iraiosub/nf-riboseq-dedup:latest'
    ].toSet(): "Unexpected or missing custom image declarations: ${images}"
    println "PASS: ${images.size()} declarations retain Docker Hub with registry=quay.io"
}
