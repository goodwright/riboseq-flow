# Resource configuration regression test

With Python 3 and Nextflow 24.10.8 on PATH:

```bash
python3 tests/check_max/test_resources.py
```

A custom executable or Java launcher can be supplied after `--nextflow`.
The test runs small local shell processes, without containers, sequencing data,
or scheduler access. It reads the repository's actual `conf/base.config` and
checks capped, below-cap and unset-cap CPU, memory and time values. Temporary
fixtures are removed after each case. The capped case reproduces the missing
`ScriptBinding.check_max()` exception before the fix.
