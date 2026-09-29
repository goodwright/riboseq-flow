"""Run tiny local processes to exercise the real base.config resource helper."""
import argparse
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MAIN = '''nextflow.enable.dsl=2
process RESOURCE_CHECK {
    label 'process_high'
    output: stdout
    script:
    """
    echo '${task.cpus}|${task.memory}|${task.time}'
    """
}
workflow { RESOURCE_CHECK().view() }
'''
CAPS = """params.max_cpus = 2
params.max_memory = '64 MB'
params.max_time = '1 min'
"""
# Evaluate below-cap and unset-cap paths without requesting production-sized
# resources. Keep these closures in the same config scope as the actual helper.
SMALL_REQUESTS = """
process {
    withLabel: process_high {
        cpus = { check_max(1, 'cpus') }
        memory = { check_max(16.MB, 'memory') }
        time = { check_max(30.s, 'time') }
    }
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nextflow', nargs=argparse.REMAINDER, default=['nextflow'],
                        help='Nextflow executable or java -jar command (last option)')
    args = parser.parse_args()
    base = (ROOT / 'conf/base.config').read_text()
    cases = [
        ('capped', CAPS, '', '2|64 MB|1m'),
        ('below-cap', CAPS, SMALL_REQUESTS, '1|16 MB|30s'),
        ('unset-cap', '', SMALL_REQUESTS, '1|16 MB|30s'),
    ]
    for name, caps, requests, expected in cases:
        with tempfile.TemporaryDirectory(prefix=f'riboseq-{name}-') as tmp:
            work = Path(tmp)
            (work / 'conf').mkdir()
            (work / 'conf/base.config').write_text(base + requests)
            (work / 'main.nf').write_text(MAIN)
            (work / 'nextflow.config').write_text(
                caps + "includeConfig 'conf/base.config'\n"
                "process.errorStrategy = 'terminate'\n"
            )
            result = subprocess.run(
                args.nextflow + ['run', 'main.nf', '-ansi-log', 'false'],
                cwd=work, capture_output=True, text=True, timeout=180,
            )
            output = result.stdout + result.stderr
            if result.returncode or expected not in output.splitlines():
                raise RuntimeError(f'{name} failed (exit {result.returncode}):\n{output}')
            print(f'PASS {name}: {expected}')


if __name__ == '__main__':
    main()
