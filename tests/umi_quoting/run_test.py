import argparse, os, pathlib, subprocess, tempfile, json
p=argparse.ArgumentParser();p.add_argument('java');p.add_argument('jar');a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[2]
cases=[('regex', '^(?P<umi_1>.{2}).+?(?P<umi_2>.{5})(?P<discard_1>TAGACAGATCGGAAGAGCACACGTCT.*)$'),('string','NNNNNNNN'),('regex',"^(?P<umi_1>.{2})(?#literal ' $HOME `false` $(false)).*$")]
with tempfile.TemporaryDirectory(prefix='umi-quoting-') as temp:
 d=pathlib.Path(temp)
 for i,(method,pattern) in enumerate(cases):
  run=d/str(i);run.mkdir();input=run/'pattern.txt';input.write_text(pattern)
  # Params JSON avoids an extra shell parsing layer in the test driver.
  params=run/'params.json';params.write_text(json.dumps(dict(umi_pattern=pattern,umi_extract_method=method,test_pattern_file=str(input))))
  cmd=[a.java,'-jar',a.jar,'-C',str(root/'tests/umi_quoting/nextflow.config'),'run',str(root/'tests/umi_quoting/main.nf'),'-params-file',str(params),'-ansi-log','false']
  r=subprocess.run(cmd,cwd=run,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  print(r.stdout)
  if r.returncode:raise SystemExit(r.returncode)
  logs=list((run/'work').glob('*/*/sample.umi_extract.log'));assert len(logs)==1
  assert logs[0].read_text().startswith('PASS:')
  print('PASS case',i,method)
