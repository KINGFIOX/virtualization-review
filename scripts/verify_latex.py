#!/usr/bin/env python3
"""Check the assembled review, its source keys, figures, and PDF bounds."""
from pathlib import Path
from collections import Counter
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []
files = []

def visit(p):
    p = p.resolve()
    if not p.is_relative_to(ROOT):
        errors.append('External TeX input: '+str(p)); return
    if not p.exists():
        errors.append('Missing TeX input: '+str(p)); return
    if p in files:
        errors.append('Repeated TeX input: '+str(p)); return
    files.append(p)
    text = p.read_text(encoding='utf-8')
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        child = ROOT / name
        if not child.suffix:
            child = child.with_suffix('.tex')
        visit(child)

visit(ROOT/'main.tex')
texts = {str(p.relative_to(ROOT)):p.read_text(encoding='utf-8') for p in files}
body = '\n'.join(texts.values())
bib = (ROOT/'references.bib').read_text(encoding='utf-8')
bibkeys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+)',bib))
cites = []
for group in re.findall(r'\\cite(?:p|t|author|year)?\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}',body):
    cites += [x.strip() for x in group.split(',')]
unknown = sorted(set(cites)-bibkeys)
if unknown: errors.append('Unknown citation keys: '+str(unknown))
labels = re.findall(r'\\label\{([^}]+)\}',body)
labels += re.findall(r'label=\{([^}]+)\}',body)  # lstlisting 等环境的选项式 label
refs = re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',body)
missing_refs = sorted(set(refs)-set(labels))
if missing_refs: errors.append('Unknown reference labels: '+str(missing_refs))
duplicates = [key for key,n in Counter(labels).items() if n>1]
if duplicates: errors.append('Duplicate labels: '+str(duplicates))
chapters = {}
for name in ['00-intro','01-software','02-hardware','03-nested']:
    text = texts.get('chapters/'+name+'.tex','')
    sections = re.findall(r'\\section\{([^}]+)\}',text)
    subsections = re.findall(r'\\subsection\{([^}]+)\}',text)
    cjk = len(re.findall(r'[\u4e00-\u9fff]',text))
    chapters[name] = {'title':sections,'subsections':subsections,'cjk_characters':cjk}
    if len(sections)!=1 or cjk<1000:
        errors.append('Incomplete chapter: '+name)
    if name in ['01-software','02-hardware']:
        for word in ['CPU','内存','中断','设备']:
            if not any(word in t for t in subsections):
                errors.append('Missing independent dimension '+name+': '+word)
for token in ['TODO','TBD','待补图','待补正文','待核验','此处省略']:
    if token in body: errors.append('Unresolved placeholder: '+token)
figures = re.findall(r'\\label\{(fig:[^}]+)\}',body)
if len(figures)!=4: errors.append('Expected 4 figures, got '+str(len(figures)))
if not (ROOT/'build/main.pdf').exists(): errors.append('No compiled PDF')

# Bound-check actual PDF text. The header/footer are legitimate page content.
subprocess.run(['pdftotext','-bbox-layout',str(ROOT/'build/main.pdf'),str(ROOT/'build/main-bbox.html')],check=True)
doc = ET.parse(ROOT/'build/main-bbox.html')
ns = {'x':'http://www.w3.org/1999/xhtml'}
pages = doc.findall('.//x:page',ns)
bound_issues=[]
for n,page in enumerate(pages,1):
    width=float(page.attrib['width']);height=float(page.attrib['height'])
    for word in page.findall('.//x:word',ns):
        box=[float(word.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
        if box[0]<-1 or box[1]<-1 or box[2]>width+1 or box[3]>height+1:
            bound_issues.append({'page':n,'word':word.text,'box':box})
if bound_issues: errors.append('PDF contains text outside page bounds')
diag=json.loads((ROOT/'build/main-diagnostics.json').read_text())
for field in ['undefined_citations','undefined_references','missing_characters','overfull_boxes']:
    if diag.get(field): errors.append(field+': '+str(diag[field]))

summary={
    'chapters':chapters,
    'tex_input_files':len(files),
    'figures':figures,
    'tables':re.findall(r'\\label\{(tab:[^}]+)\}',body),
    'bibliography_entries':len(bibkeys),
    'distinct_cited_sources':sorted(set(cites)),
    'citation_occurrences':len(cites),
    'pdf_pages':len(pages),
    'pdf_bounds_issues':bound_issues,
    'errors':errors,
    'passed':not errors,
}
(ROOT/'build/verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
