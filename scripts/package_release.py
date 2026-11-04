#!/usr/bin/env python3
"""Package only the reviewed manuscript and reproducible source files."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
verification = json.loads((ROOT/'build/verification.json').read_text())
if not verification.get('passed'):
    raise SystemExit('Run and pass verify_latex.py before packaging')
expected = ['00-intro','01-software','02-hardware','03-nested','frontmatter-conclusion']
usage = {}
for stem in expected:
    p = ROOT/'logs'/f'{stem}-usage.json'
    if not p.exists():
        raise SystemExit('Writer has no completion report: '+stem)
    data = json.loads(p.read_text())
    if data.get('model') != 'deepseek-v4-pro' or not data.get('completed') or data.get('failed'):
        raise SystemExit('Writer did not complete on the selected model: '+stem)
    usage[stem] = {'model': data['model'], 'api_calls':data.get('api_calls'), 'completed':data['completed']}

inputs = [ROOT/'main.tex',ROOT/'preamble.tex',ROOT/'references.bib',ROOT/'README.md']
inputs += sorted((ROOT/'chapters').glob('*.tex'))
inputs += sorted((ROOT/'figures').glob('*.tex'))
inputs += [ROOT/'scripts/build_latex.py',ROOT/'scripts/verify_latex.py']
pdf = ROOT/'build/main.pdf'
if max(p.stat().st_mtime for p in inputs if p.suffix in ['.tex','.bib']) > pdf.stat().st_mtime:
    raise SystemExit('PDF is older than a manuscript source')
if not pdf.read_bytes().startswith(b'%PDF-'):
    raise SystemExit('Output is not a PDF')
output = ROOT/'wangjin_virtualization_review.pdf'
shutil.copyfile(pdf,output)
archive = ROOT/'wangjin_virtualization_review_source.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in inputs:
        z.write(p,arcname=str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    bad = z.testzip()
    if bad:
        raise SystemExit('Archive integrity failure: '+bad)
manifest = {
    'pdf': str(output), 'pdf_pages': verification['pdf_pages'],
    'source_archive': str(archive), 'archive_members': len(inputs),
    'figures': len(verification['figures']), 'tables':len(verification['tables']),
    'bibliography_entries': verification['bibliography_entries'],
    'pdf_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
    'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
    'writer_provider':'glm-gateway-r (user-confirmed via-feilian route)',
    'writer_runs':usage,
    'verification_passed':True,
}
(ROOT/'build/release.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
