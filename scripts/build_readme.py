"""Update only the Representative papers + Datasets section in README.md.

Usage from repository root:
    python scripts/build_readme.py

Usage from scripts/:
    python build_readme.py

The script reads:
    data/papers.yml
    data/datasets.yml

It replaces only the block starting at:
    ## Representative papers
and ending before:
    ## Maintenance policy

Everything before and after that block is preserved.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


START_HEADING = "## Representative papers"
END_HEADING = "## Maintenance policy"

# Used only when papers.yml does not contain survey/collection resources.
DEFAULT_SURVEYS_AND_COLLECTIONS = [
    {
        "year": 2024,
        "venue": "arXiv",
        "title": "How NeRFs and 3D Gaussian Splatting are Reshaping SLAM: a Survey",
        "paper": "https://arxiv.org/abs/2402.13255",
        "category": "Survey",
        "summary": "Reviews neural/radiance-field SLAM progress and positions 3DGS as a key explicit radiance-field representation for SLAM.",
    },
    {
        "year": "active",
        "venue": "GitHub",
        "title": "Awesome-3DGS-SLAM",
        "paper": "https://github.com/KwanWaiPang/Awesome-3DGS-SLAM",
        "category": "Collection",
        "summary": "Useful cross-check list covering image-, LiDAR-, and event-based 3DGS-SLAM works.",
    },
]


def repo_root() -> Path:
    """Return repository root whether the script runs from root or scripts/."""
    here = Path(__file__).resolve()
    if here.parent.name == "scripts":
        return here.parents[1]
    # Fallback: script may be copied to repo root.
    if (here.parent / "data").exists():
        return here.parent
    return here.parents[1]


def load_yaml(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    if not isinstance(data, list):
        raise ValueError(f"Expected a list in {path}, got {type(data).__name__}")
    return [x for x in data if isinstance(x, dict)]


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, tuple):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    # Split only simple comma-separated scalar fields.
    return [x.strip() for x in text.split(",") if x.strip()]


def join(value: Any, sep: str = ", ") -> str:
    items = as_list(value)
    return sep.join(items)


def md_escape(text: Any) -> str:
    """Escape Markdown table-sensitive characters."""
    if text is None:
        return ""
    s = str(text).replace("\n", " ").replace("\r", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s.replace("|", "\\|")


def md_link(label: str, url: Any) -> str:
    label = md_escape(label)
    url = str(url or "").strip()
    if not url or url.upper() == "TBD":
        return label or "TBD"
    return f"[{label}]({url})"


def link_or_tbd(label: str, url: Any) -> str:
    url = str(url or "").strip()
    if not url or url.upper() == "TBD":
        return "TBD"
    return f"[{label}]({url})"


def searchable_text(p: dict[str, Any]) -> str:
    fields = [
        p.get("title"),
        p.get("category"),
        p.get("modality"),
        p.get("representation"),
        p.get("tags"),
        p.get("summary"),
        p.get("abstract"),
        p.get("focus"),
    ]
    return " ".join(join(x) if isinstance(x, list) else str(x or "") for x in fields).lower()


def is_survey_or_collection(p: dict[str, Any]) -> bool:
    text = searchable_text(p)
    kind = str(p.get("kind") or p.get("type") or p.get("resource_type") or "").lower()
    return any(k in text or k in kind for k in ["survey", "collection", "awesome", "benchmark list"])


def is_3dgs_related(p: dict[str, Any]) -> bool:
    """Keep 3DGS/Gaussian-related works and drop NeRF-only entries."""
    text = searchable_text(p)
    positive = [
        "3dgs",
        "gaussian",
        "splat",
        "splatting",
        "2dgs",
        "surfel",
        "gs-slam",
    ]
    if any(k in text for k in positive):
        return True
    # Keep explicit surveys/collections because the section may cite a survey that mentions NeRF in the title.
    return is_survey_or_collection(p)


def is_specialized(p: dict[str, Any]) -> bool:
    text = searchable_text(p)
    keywords = [
        "dynamic",
        "semantic",
        "language",
        "open-vocabulary",
        "large-scale",
        "large scale",
        "outdoor",
        "driving",
        "autonomous",
        "urban",
        "lidar",
        "event",
        "localization",
        "relocalization",
        "multi-agent",
        "collaborative",
        "multimodal",
        "multi-modal",
        "compression",
        "compact",
        "foundation",
        "object",
        "loop closure",
        "long-term",
        "robust",
    ]
    return any(k in text for k in keywords)


def classify_paper(p: dict[str, Any]) -> str:
    """Return README group: survey, rgbd, mono, or specialized.

    You can override the automatic rules in data/papers.yml with:
        readme_group: rgbd
    Valid values: survey, rgbd, mono, specialized.
    """
    override = str(p.get("readme_group") or "").strip().lower()
    aliases = {
        "surveys": "survey",
        "collection": "survey",
        "collections": "survey",
        "rgb-d": "rgbd",
        "rgb_d": "rgbd",
        "dense": "rgbd",
        "monocular": "mono",
        "rgb-only": "mono",
        "multi-sensor": "mono",
        "special": "specialized",
    }
    override = aliases.get(override, override)
    if override in {"survey", "rgbd", "mono", "specialized"}:
        return override

    if is_survey_or_collection(p):
        return "survey"

    text = searchable_text(p)
    modality = " ".join(as_list(p.get("modality"))).lower()

    if is_specialized(p):
        return "specialized"

    mono_keywords = [
        "monocular",
        "rgb-only",
        "rgb only",
        "stereo",
        "vio",
        "visual-inertial",
        "visual inertial",
        "multi-sensor",
        "multisensor",
    ]
    if any(k in modality or k in text for k in mono_keywords):
        return "mono"

    if "rgb-d" in modality or "rgbd" in modality or "depth" in modality:
        return "rgbd"

    # Unknown-but-3DGS papers go to specialized so they are not lost.
    return "specialized"


def sort_key(p: dict[str, Any]) -> tuple[int, str, str]:
    year = p.get("year", 0)
    try:
        y = int(year)
    except Exception:
        y = -1
    return (-y, str(p.get("venue") or ""), str(p.get("title") or ""))


def paper_title_cell(p: dict[str, Any]) -> str:
    title = p.get("title") or p.get("name") or p.get("id") or "Untitled"
    # Prefer project page for project-style papers when paper is missing; otherwise paper URL.
    url = p.get("paper") or p.get("project") or p.get("url") or ""
    return md_link(str(title), url)


def render_survey_table(items: list[dict[str, Any]]) -> str:
    rows = [
        "| Year | Venue | Paper / Resource | Category | Summary |",
        "|---:|---|---|---|---|",
    ]
    for p in sorted(items, key=sort_key):
        rows.append(
            "| {year} | {venue} | {paper} | {category} | {summary} |".format(
                year=md_escape(p.get("year", "")),
                venue=md_escape(p.get("venue", "")),
                paper=paper_title_cell(p),
                category=md_escape(p.get("category") or p.get("type") or p.get("kind") or "Resource"),
                summary=md_escape(p.get("summary") or p.get("abstract") or ""),
            )
        )
    return "\n".join(rows)


def render_standard_paper_table(items: list[dict[str, Any]]) -> str:
    rows = [
        "| Year | Venue | Paper | Code | Modality | Representation | Datasets | Metrics | Summary | Local Eval |",
        "|---:|---|---|---|---|---|---|---|---|---|",
    ]
    for p in sorted(items, key=sort_key):
        rows.append(
            "| {year} | {venue} | {paper} | {code} | {modality} | {representation} | {datasets} | {metrics} | {summary} | {local_eval} |".format(
                year=md_escape(p.get("year", "")),
                venue=md_escape(p.get("venue", "")),
                paper=paper_title_cell(p),
                code=link_or_tbd("code", p.get("code")),
                modality=md_escape(join(p.get("modality"))),
                representation=md_escape(p.get("representation", "")),
                datasets=md_escape(join(p.get("datasets"))),
                metrics=md_escape(join(p.get("metrics"))),
                summary=md_escape(p.get("summary") or p.get("abstract") or ""),
                local_eval=md_escape(p.get("local_eval") or "not tested"),
            )
        )
    return "\n".join(rows)


def render_specialized_table(items: list[dict[str, Any]]) -> str:
    rows = [
        "| Year | Venue | Paper | Code | Modality | Focus | Datasets | Summary | Local Eval |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for p in sorted(items, key=sort_key):
        focus = p.get("focus") or p.get("category") or join(p.get("tags"))
        rows.append(
            "| {year} | {venue} | {paper} | {code} | {modality} | {focus} | {datasets} | {summary} | {local_eval} |".format(
                year=md_escape(p.get("year", "")),
                venue=md_escape(p.get("venue", "")),
                paper=paper_title_cell(p),
                code=link_or_tbd("code", p.get("code")),
                modality=md_escape(join(p.get("modality"))),
                focus=md_escape(focus),
                datasets=md_escape(join(p.get("datasets"))),
                summary=md_escape(p.get("summary") or p.get("abstract") or ""),
                local_eval=md_escape(p.get("local_eval") or "not tested"),
            )
        )
    return "\n".join(rows)


def render_datasets_table(datasets: list[dict[str, Any]]) -> str:
    rows = [
        "| Dataset | Type | Sensors / data | Ground truth | Common use in 3DGS-SLAM | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for d in sorted(datasets, key=lambda x: str(x.get("name") or x.get("id") or "").lower()):
        name = d.get("name") or d.get("id") or "Unnamed dataset"
        url = d.get("url") or d.get("link") or ""
        rows.append(
            "| {dataset} | {type} | {sensors} | {gt} | {common_use} | {notes} |".format(
                dataset=md_link(str(name), url),
                type=md_escape(d.get("type", "")),
                sensors=md_escape(d.get("sensors") or d.get("sensors_data") or d.get("data") or ""),
                gt=md_escape(d.get("gt") or d.get("ground_truth") or ""),
                common_use=md_escape(d.get("common_use") or d.get("common_use_in_3dgs_slam") or ""),
                notes=md_escape(d.get("notes", "")),
            )
        )
    return "\n".join(rows)


def render_representative_section(papers: list[dict[str, Any]], datasets: list[dict[str, Any]]) -> str:
    papers = [p for p in papers if is_3dgs_related(p)]

    surveys = [p for p in papers if classify_paper(p) == "survey"]
    if not surveys:
        surveys = DEFAULT_SURVEYS_AND_COLLECTIONS

    groups = {
        "rgbd": [p for p in papers if classify_paper(p) == "rgbd"],
        "mono": [p for p in papers if classify_paper(p) == "mono"],
        "specialized": [p for p in papers if classify_paper(p) == "specialized"],
    }

    return "\n\n".join(
        [
            "## Representative papers",
            "> This section is generated from `data/papers.yml` and `data/datasets.yml`. Do not edit the tables manually. Use `readme_group` in `data/papers.yml` to override automatic classification.",
            "### Surveys and collections\n\n" + render_survey_table(surveys),
            "### RGB-D / dense SLAM\n\n" + render_standard_paper_table(groups["rgbd"]),
            "### Monocular / RGB-only / multi-sensor\n\n" + render_standard_paper_table(groups["mono"]),
            "### Dynamic, semantic, large-scale, and specialized settings\n\n" + render_specialized_table(groups["specialized"]),
            "## Datasets\n\n" + render_datasets_table(datasets),
        ]
    )


def replace_section(readme_text: str, generated_section: str) -> str:
    start = readme_text.find(START_HEADING)
    if start == -1:
        raise ValueError(f"Cannot find start heading: {START_HEADING}")

    end = readme_text.find(END_HEADING, start)
    if end == -1:
        raise ValueError(f"Cannot find end heading after Representative papers: {END_HEADING}")

    before = readme_text[:start].rstrip()
    after = readme_text[end:].lstrip()
    return before + "\n\n" + generated_section.rstrip() + "\n\n" + after


def main() -> None:
    root = repo_root()
    readme_path = root / "README.md"
    papers_path = root / "data" / "papers.yml"
    datasets_path = root / "data" / "datasets.yml"

    readme = readme_path.read_text(encoding="utf-8")
    papers = load_yaml(papers_path)
    datasets = load_yaml(datasets_path)

    generated = render_representative_section(papers, datasets)
    updated = replace_section(readme, generated)
    readme_path.write_text(updated, encoding="utf-8", newline="\n")

    print(f"Updated {readme_path}")
    print(f"Papers loaded: {len(papers)}")
    print(f"Datasets loaded: {len(datasets)}")


if __name__ == "__main__":
    main()
