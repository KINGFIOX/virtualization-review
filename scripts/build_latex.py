#!/usr/bin/env python3
"""Compile XeLaTeX + BibTeX and summarize genuine diagnostics."""
from pathlib import Path
import argparse
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT/'build'
BUILD.mkdir(exist_ok=True)

def command(argv, logfile):
    result = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    logfile.write_text(result.stdout, encoding='utf-8')
    if result.returncode:
        print(result.stdout[-10000:])
        raise SystemExit(result.returncode)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stem', nargs='?', default='main')
    args = parser.parse_args()
    stem = args.stem
    if not re.fullmatch(r'[a-zA-Z0-9_-]+',stem):
        raise SystemExit('Invalid basename')
    xe = ['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory=build',stem+'.tex']
    command(xe, BUILD/f'{stem}-pass1.txt')
    command(['bibtex',f'build/{stem}'], BUILD/f'{stem}-bibtex.txt')
    command(xe, BUILD/f'{stem}-pass2.txt')
    command(xe, BUILD/f'{stem}-pass3.txt')
    pdf = BUILD/f'{stem}.pdf'
    command(['pdftotext','-layout',str(pdf),str(BUILD/f'{stem}.txt')],BUILD/f'{stem}-pdftotext.txt')
    info = subprocess.run(['pdfinfo',str(pdf)],text=True,capture_output=True,check=True).stdout
    (BUILD/f'{stem}-pdfinfo.txt').write_text(info,encoding='utf-8')
    log=(BUILD/f'{stem}.log').read_text(encoding='utf-8',errors='replace')
    diagnostics={
        'pdf':str(pdf),'bytes':pdf.stat().st_size,
        'pages':int(re.search(r'Pages:\s+(\d+)',info).group(1)),
        'undefined_citations':re.findall(r'.*Citation.*undefined.*',log),
        'undefined_references':re.findall(r'.*Reference.*undefined.*',log),
        'missing_characters':re.findall(r'.*Missing character:.*',log),
        'overfull_boxes':re.findall(r'Overfull \\[hv]box.*',log),
        'latex_warnings':re.findall(r'.*(?:LaTeX|Package .*?) Warning:.*',log),
    }
    (BUILD/f'{stem}-diagnostics.json').write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(diagnostics,ensure_ascii=False,indent=2))
    if any(diagnostics[x] for x in ['undefined_citations','undefined_references','missing_characters']):
        raise SystemExit(2)

if __name__ == '__main__':
    main()
