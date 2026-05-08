#!/usr/bin/env python3
"""Regenerate the embedded public data inside docs/index.html from data/*.yml.

This script intentionally ignores private/results.local.csv and all *.local.* files.
"""
from pathlib import Path
import json, re, yaml

ROOT = Path(__file__).resolve().parents[1]
html_path = ROOT / 'docs' / 'index.html'
papers = yaml.safe_load((ROOT / 'data' / 'papers.yml').read_text(encoding='utf-8'))
datasets = yaml.safe_load((ROOT / 'data' / 'datasets.yml').read_text(encoding='utf-8'))
for p in papers:
    if p.get('thumbnail','').startswith('docs/'):
        p['thumbnail'] = p['thumbnail'].replace('docs/','',1)
site_datasets = [dict(name=d['name'], type=d['type'], url=d['url'], sensors=d['sensors'], gt=d['gt'], notes=f"{d['common_use']}. {d['notes']}") for d in datasets]
text = html_path.read_text(encoding='utf-8')
text = re.sub(r"    const papers = .*?;\n\n    const datasets = ", "    const papers = " + json.dumps(papers, ensure_ascii=False, indent=6) + ";\n\n    const datasets = ", text, flags=re.S)
text = re.sub(r"    const datasets = .*?;\n\n    const state = ", "    const datasets = " + json.dumps(site_datasets, ensure_ascii=False, indent=6) + ";\n\n    const state = ", text, flags=re.S)
html_path.write_text(text, encoding='utf-8')
print(f"Embedded {len(papers)} papers and {len(site_datasets)} datasets into docs/index.html")
