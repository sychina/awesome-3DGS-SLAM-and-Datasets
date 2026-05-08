#!/usr/bin/env python3
"""Regenerate the embedded public data inside docs/index.html from data/*.yml.

This script intentionally ignores private/results.local.csv and all *.local.* files.
It is tolerant to small schema differences in datasets.yml, for example:
- gt or ground_truth
- url or link
- sensors or sensors_data or sensors_or_data
- common_use or common_use_in_3dgs_slam
"""
from pathlib import Path
import json
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "docs" / "index.html"
PAPERS_PATH = ROOT / "data" / "papers.yml"
DATASETS_PATH = ROOT / "data" / "datasets.yml"


def load_yaml(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or []


def first_non_empty(item, keys, default=""):
    for key in keys:
        value = item.get(key)
        if value is not None and value != "":
            return value
    return default


def as_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def normalize_dataset(d):
    name = first_non_empty(d, ["name", "dataset", "title"], "Unknown dataset")
    dataset_type = first_non_empty(d, ["type", "category"], "")
    url = first_non_empty(d, ["url", "link", "homepage", "website"], "")
    sensors = first_non_empty(d, ["sensors", "sensors_data", "sensors_or_data", "data", "modalities"], "")
    gt = first_non_empty(d, ["gt", "ground_truth", "groundtruth", "ground_truth_type"], "")
    common_use = first_non_empty(d, ["common_use", "common_use_in_3dgs_slam", "usage", "use"], "")
    notes = first_non_empty(d, ["notes", "note", "description", "summary"], "")

    note_parts = [as_text(common_use), as_text(notes)]
    note_text = ". ".join(part.strip().rstrip(".") for part in note_parts if part and str(part).strip())

    return {
        "name": as_text(name),
        "type": as_text(dataset_type),
        "url": as_text(url),
        "sensors": as_text(sensors),
        "gt": as_text(gt),
        "notes": note_text,
    }


def main():
    papers = load_yaml(PAPERS_PATH)
    datasets = load_yaml(DATASETS_PATH)

    for p in papers:
        thumb = p.get("thumbnail", "")
        if isinstance(thumb, str) and thumb.startswith("docs/"):
            p["thumbnail"] = thumb.replace("docs/", "", 1)

    site_datasets = [normalize_dataset(d) for d in datasets]

    text = HTML_PATH.read_text(encoding="utf-8")

    papers_pattern = r"    const papers = .*?;\n\n    const datasets = "
    datasets_pattern = r"    const datasets = .*?;\n\n    const state = "

    if not re.search(papers_pattern, text, flags=re.S):
        raise RuntimeError("Could not find the 'const papers' block in docs/index.html")
    if not re.search(datasets_pattern, text, flags=re.S):
        raise RuntimeError("Could not find the 'const datasets' block in docs/index.html")

    text = re.sub(
        papers_pattern,
        "    const papers = " + json.dumps(papers, ensure_ascii=False, indent=6) + ";\n\n    const datasets = ",
        text,
        flags=re.S,
    )
    text = re.sub(
        datasets_pattern,
        "    const datasets = " + json.dumps(site_datasets, ensure_ascii=False, indent=6) + ";\n\n    const state = ",
        text,
        flags=re.S,
    )

    HTML_PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"Embedded {len(papers)} papers and {len(site_datasets)} datasets into docs/index.html")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
