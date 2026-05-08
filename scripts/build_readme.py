"""Minimal README generator placeholder.
Install PyYAML, then extend this script to render README from data/papers.yml and data/datasets.yml.
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(name: str):
    return yaml.safe_load((ROOT / 'data' / name).read_text(encoding='utf-8'))

if __name__ == '__main__':
    papers = load_yaml('papers.yml')
    datasets = load_yaml('datasets.yml')
    print(f'Loaded {len(papers)} papers and {len(datasets)} datasets.')
    print('Extend this script to render README sections from Jinja2 templates.')
