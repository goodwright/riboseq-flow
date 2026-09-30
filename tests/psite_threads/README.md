# P-site launcher regression

Run `nextflow -C tests/psite_threads/nextflow.config run tests/psite_threads/main.nf`
from the repository, with hostile inherited thread values (e.g. all five thread
variables set to 192). The test imports the production module, executes its
actual shell script, and substitutes only Rscript. The stub fails unless all
native thread controls are one and the scientific arguments remain unchanged.

This tests Nextflow rendering, shell environment overrides and runtime-file
publication. It does not execute riboWaltz or prove that the native crash is
fixed. Validate the real sample and annotation in Flow after deployment; inspect
psite_runtime.txt, stderr stage markers, P-site outputs and downstream QC.
