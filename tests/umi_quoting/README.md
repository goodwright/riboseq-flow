# UMI command-quoting regression

Run `python3 tests/umi_quoting/run_test.py /path/to/java /path/to/nextflow.jar`.
The test imports the production Nextflow module and substitutes only umi_tools
with an argv checker. It exercises the U2OS split-UMI regex, the HCT string
pattern, and literal apostrophes/dollar signs/backticks/command substitutions.
It checks exact argument preservation, not biological extraction correctness.

Pass raw regex text as umi_pattern. Do not include shell quote characters in
parameter values: the module now owns shell quoting. Flow pilot validation is
still required after deployment.
