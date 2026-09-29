# Container registry regression test

Run with Nextflow 24.10.8:

```bash
nextflow -C tests/container_registry/nextflow.config run tests/container_registry/main.nf -ansi-log false
```

The test reads the custom image declarations from `modules/local`, checks that
all specify Docker Hub explicitly, and verifies that Nextflow's image resolver
preserves those addresses when the configured default registry is `quay.io`.
It launches no tasks and does not require Docker, image downloads or biological
data. Container availability and execution on a worker require a separate pilot.
