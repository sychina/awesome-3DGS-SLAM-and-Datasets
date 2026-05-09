#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate data/papers.yml and data/datasets.yml for the 3DGS-SLAM literature hub.

Usage:
    python scripts/validate_data.py
    python scripts/validate_data.py --strict

What this script checks:
    1. YAML can be loaded with UTF-8.
    2. Paper IDs are unique.
    3. Dataset IDs and names are unique.
    4. Paper titles are not duplicated after normalization.
    5. arXiv IDs are not duplicated.
    6. DOIs are not duplicated.
    7. Paper referenced datasets exist in data/datasets.yml.
    8. readme_group values are valid.
    9. local_eval values are valid.
    10. Thumbnail paths exist if provided.
    11. Obvious NeRF-only papers are warned or blocked.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.yml"
DATASETS_PATH = ROOT / "data" / "datasets.yml"
DOCS_PATH = ROOT / "docs"


VALID_README_GROUPS = {
    "survey",
    "rgbd",
    "mono",
    "specialized",
}

VALID_LOCAL_EVAL = {
    "",
    "not tested",
    "reproduce pending",
    "tested locally",
    "failed locally",
    "partial reproduced",
    "paper only",
}

RECOMMENDED_PAPER_FIELDS = {
    "id",
    "title",
    "year",
    "venue",
    "summary",
}

OPTIONAL_LINK_FIELDS = {
    "paper",
    "code",
    "project",
    "video",
}

NEURAL_ONLY_HINTS = {
    "nerf",
    "neural radiance field",
    "radiance fields",
    "neural fields",
    "implicit neural",
}

GAUSSIAN_HINTS = {
    "3dgs",
    "3d gaussian",
    "gaussian splatting",
    "gaussian surfel",
    "gaussian surfels",
    "2d gaussian",
    "splat",
    "splatting",
    "gaussian map",
}


class ValidationReport:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def print(self) -> None:
        if self.errors:
            print("\nErrors:")
            for item in self.errors:
                print(f"  [ERROR] {item}")

        if self.warnings:
            print("\nWarnings:")
            for item in self.warnings:
                print(f"  [WARN] {item}")

        if not self.errors and not self.warnings:
            print("Validation passed. No errors or warnings.")
        elif not self.errors:
            print(f"\nValidation finished with {len(self.warnings)} warning(s) and no errors.")
        else:
            print(
                f"\nValidation failed with {len(self.errors)} error(s) "
                f"and {len(self.warnings)} warning(s)."
            )


def load_yaml_list(path: Path, report: ValidationReport) -> List[Dict[str, Any]]:
    if not path.exists():
        report.error(f"Missing file: {path.relative_to(ROOT)}")
        return []

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        report.error(
            f"Cannot decode {path.relative_to(ROOT)} as UTF-8: {exc}. "
            "Please save the file as UTF-8."
        )
        return []
    except yaml.YAMLError as exc:
        report.error(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}")
        return []

    if data is None:
        return []

    if not isinstance(data, list):
        report.error(f"{path.relative_to(ROOT)} must be a YAML list.")
        return []

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            report.error(
                f"{path.relative_to(ROOT)} item #{idx + 1} must be a mapping/dict."
            )
            continue
        normalized.append(item)

    return normalized


def as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, tuple):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text:
        return []

    # Support comma-separated strings such as "Replica, TUM RGB-D, ScanNet".
    if "," in text:
        return [part.strip() for part in text.split(",") if part.strip()]

    return [text]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def normalize_id(text: Any) -> str:
    text = as_text(text).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def normalize_title(title: Any) -> str:
    text = as_text(title).lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_dataset_name(name: Any) -> str:
    text = as_text(name).lower()
    text = text.replace("++", " plus plus")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_arxiv_id_from_text(text: str) -> str:
    if not text:
        return ""

    patterns = [
        r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?",
        r"arxiv:([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)

    return ""


def extract_doi_from_text(text: str) -> str:
    if not text:
        return ""

    match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(0).lower().rstrip(".,;)")

    return ""


def collect_text_from_paper(paper: Dict[str, Any]) -> str:
    parts: List[str] = []

    for key in [
        "title",
        "paper",
        "url",
        "link",
        "doi",
        "arxiv",
        "project",
        "code",
        "summary",
        "abstract",
    ]:
        value = paper.get(key)
        if value:
            parts.append(as_text(value))

    return " ".join(parts)


def get_paper_display(paper: Dict[str, Any], index: int) -> str:
    pid = paper.get("id", "<missing-id>")
    year = paper.get("year", "<missing-year>")
    title = paper.get("title", "<missing-title>")
    return f"#{index + 1}: {pid} | {year} | {title}"


def report_duplicates(
    name: str,
    bucket: Dict[str, List[int]],
    items: List[Dict[str, Any]],
    report: ValidationReport,
    severity: str = "error",
) -> None:
    for key, indices in sorted(bucket.items()):
        if not key or len(indices) <= 1:
            continue

        lines = [f"Duplicate {name}: {key}"]
        for idx in indices:
            lines.append(f"    - {get_paper_display(items[idx], idx)}")
        message = "\n".join(lines)

        if severity == "warning":
            report.warn(message)
        else:
            report.error(message)


def looks_like_nerf_only(paper: Dict[str, Any]) -> bool:
    text = " ".join(
        [
            as_text(paper.get("title")),
            as_text(paper.get("summary")),
            as_text(paper.get("abstract")),
            as_text(paper.get("representation")),
            " ".join(as_list(paper.get("tags"))),
        ]
    ).lower()

    has_nerf_hint = any(hint in text for hint in NEURAL_ONLY_HINTS)
    has_gaussian_hint = any(hint in text for hint in GAUSSIAN_HINTS)

    return has_nerf_hint and not has_gaussian_hint


def validate_required_fields(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    for idx, paper in enumerate(papers):
        for field in RECOMMENDED_PAPER_FIELDS:
            if field not in paper or as_text(paper.get(field)) == "":
                report.warn(
                    f"Paper missing recommended field '{field}': "
                    f"{get_paper_display(paper, idx)}"
                )

        if not paper.get("paper") and not paper.get("project"):
            report.warn(
                "Paper has neither 'paper' nor 'project' link: "
                f"{get_paper_display(paper, idx)}"
            )

        year = paper.get("year")
        if year not in (None, "", "active", "TBD"):
            try:
                year_int = int(year)
                if year_int < 1990 or year_int > 2035:
                    report.warn(
                        f"Suspicious year '{year}' in {get_paper_display(paper, idx)}"
                    )
            except Exception:
                report.warn(
                    f"Year should be an integer, 'active', or 'TBD': "
                    f"{get_paper_display(paper, idx)}"
                )


def validate_paper_duplicates(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    ids: Dict[str, List[int]] = defaultdict(list)
    titles: Dict[str, List[int]] = defaultdict(list)
    arxiv_ids: Dict[str, List[int]] = defaultdict(list)
    dois: Dict[str, List[int]] = defaultdict(list)

    for idx, paper in enumerate(papers):
        pid = normalize_id(paper.get("id"))
        title = normalize_title(paper.get("title"))

        if pid:
            ids[pid].append(idx)
        else:
            report.error(f"Paper missing required id: {get_paper_display(paper, idx)}")

        if title:
            titles[title].append(idx)

        text = collect_text_from_paper(paper)

        arxiv_id = extract_arxiv_id_from_text(text)
        if arxiv_id:
            arxiv_ids[arxiv_id].append(idx)

        doi = as_text(paper.get("doi")) or extract_doi_from_text(text)
        if doi:
            dois[doi.lower()].append(idx)

    report_duplicates("paper id", ids, papers, report, severity="error")
    report_duplicates("paper title", titles, papers, report, severity="warning")
    report_duplicates("arXiv ID", arxiv_ids, papers, report, severity="warning")
    report_duplicates("DOI", dois, papers, report, severity="warning")


def validate_readme_group(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    for idx, paper in enumerate(papers):
        group = as_text(paper.get("readme_group"))
        if group and group not in VALID_README_GROUPS:
            report.warn(
                f"Invalid readme_group '{group}' in {get_paper_display(paper, idx)}. "
                f"Valid values: {sorted(VALID_README_GROUPS)}"
            )


def validate_local_eval(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    for idx, paper in enumerate(papers):
        value = as_text(paper.get("local_eval")).lower()
        if value not in VALID_LOCAL_EVAL:
            report.warn(
                f"Unexpected local_eval '{paper.get('local_eval')}' in "
                f"{get_paper_display(paper, idx)}. "
                f"Suggested values: {sorted(v for v in VALID_LOCAL_EVAL if v)}"
            )


def validate_links(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    for idx, paper in enumerate(papers):
        for field in OPTIONAL_LINK_FIELDS:
            value = as_text(paper.get(field))
            if not value:
                continue

            if not (
                value.startswith("http://")
                or value.startswith("https://")
                or value.startswith("assets/")
                or value.startswith("./")
                or value.startswith("../")
            ):
                report.warn(
                    f"Suspicious link in field '{field}' for "
                    f"{get_paper_display(paper, idx)}: {value}"
                )


def validate_thumbnails(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    for idx, paper in enumerate(papers):
        thumbnail = as_text(paper.get("thumbnail"))
        if not thumbnail:
            continue

        if thumbnail.startswith("http://") or thumbnail.startswith("https://"):
            continue

        # In docs/index.html, paths like assets/thumbnails/a.jpg are relative to docs/.
        possible_paths = [
            DOCS_PATH / thumbnail,
            ROOT / thumbnail,
        ]

        if not any(path.exists() for path in possible_paths):
            report.warn(
                f"Thumbnail file not found for {get_paper_display(paper, idx)}: "
                f"{thumbnail}"
            )


def validate_3dgs_only(papers: List[Dict[str, Any]], report: ValidationReport) -> None:
    for idx, paper in enumerate(papers):
        if looks_like_nerf_only(paper):
            report.warn(
                "Possible NeRF-only paper detected. Please confirm it is really "
                f"3DGS-related: {get_paper_display(paper, idx)}"
            )


def validate_datasets(
    datasets: List[Dict[str, Any]],
    report: ValidationReport,
) -> Dict[str, str]:
    ids: Dict[str, List[int]] = defaultdict(list)
    names: Dict[str, List[int]] = defaultdict(list)

    dataset_lookup: Dict[str, str] = {}

    for idx, dataset in enumerate(datasets):
        did = normalize_id(dataset.get("id"))
        name = as_text(dataset.get("name"))
        normalized_name = normalize_dataset_name(name)

        if not did:
            report.warn(f"Dataset #{idx + 1} missing recommended field 'id'.")
        else:
            ids[did].append(idx)
            dataset_lookup[did] = name

        if not name:
            report.error(f"Dataset #{idx + 1} missing required field 'name'.")
        else:
            names[normalized_name].append(idx)
            dataset_lookup[normalized_name] = name

        for field in ["type", "url"]:
            if field not in dataset or as_text(dataset.get(field)) == "":
                report.warn(f"Dataset '{name or idx + 1}' missing recommended field '{field}'.")

        url = as_text(dataset.get("url") or dataset.get("link"))
        if url and not (url.startswith("http://") or url.startswith("https://")):
            report.warn(f"Dataset '{name}' has suspicious url: {url}")

    for key, indices in sorted(ids.items()):
        if key and len(indices) > 1:
            lines = [f"Duplicate dataset id: {key}"]
            for idx in indices:
                lines.append(
                    f"    - #{idx + 1}: {datasets[idx].get('id')} | {datasets[idx].get('name')}"
                )
            report.error("\n".join(lines))

    for key, indices in sorted(names.items()):
        if key and len(indices) > 1:
            lines = [f"Duplicate dataset name: {key}"]
            for idx in indices:
                lines.append(
                    f"    - #{idx + 1}: {datasets[idx].get('id')} | {datasets[idx].get('name')}"
                )
            report.warn("\n".join(lines))

    return dataset_lookup


def validate_paper_dataset_refs(
    papers: List[Dict[str, Any]],
    dataset_lookup: Dict[str, str],
    report: ValidationReport,
) -> None:
    if not dataset_lookup:
        return

    for idx, paper in enumerate(papers):
        paper_datasets = as_list(paper.get("datasets"))
        for dataset_name in paper_datasets:
            normalized = normalize_dataset_name(dataset_name)
            dataset_id = normalize_id(dataset_name)

            if normalized not in dataset_lookup and dataset_id not in dataset_lookup:
                report.warn(
                    f"Paper references dataset not found in data/datasets.yml: "
                    f"'{dataset_name}' in {get_paper_display(paper, idx)}"
                )


def validate_private_results_not_loaded(report: ValidationReport) -> None:
    private_dir = ROOT / "private"
    if private_dir.exists():
        report.warn(
            "private/ directory exists. This is fine locally, but make sure it is ignored "
            "by .gitignore and never published to docs/."
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    args = parser.parse_args()

    report = ValidationReport()

    papers = load_yaml_list(PAPERS_PATH, report)
    datasets = load_yaml_list(DATASETS_PATH, report)

    validate_required_fields(papers, report)
    validate_paper_duplicates(papers, report)
    validate_readme_group(papers, report)
    validate_local_eval(papers, report)
    validate_links(papers, report)
    validate_thumbnails(papers, report)
    validate_3dgs_only(papers, report)

    dataset_lookup = validate_datasets(datasets, report)
    validate_paper_dataset_refs(papers, dataset_lookup, report)

    validate_private_results_not_loaded(report)

    print("\nSummary:")
    print(f"  Papers:   {len(papers)}")
    print(f"  Datasets: {len(datasets)}")

    report.print()

    if report.errors:
        return 1

    if args.strict and report.warnings:
        print("\nStrict mode enabled: warnings are treated as failures.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())