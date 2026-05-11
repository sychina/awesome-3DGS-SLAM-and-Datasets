#!/usr/bin/env python3
"""
自动为 3DGS-SLAM 论文生成缩略图（小体积 + 小尺寸版）。
- 默认直接使用 paper 链接（包括 PDF），截取 PDF 第一页作为封面。
- 使用 --use-abs 可将 arxiv/pdf 换成 /abs 摘要页。
- 使用 --force 强制重新截图所有论文。
- 缩略图尺寸：800x1100 视口；目标体积 ≤ 150 KB。

用法：
  python scripts/generate_thumbnails.py                 # 默认：直接使用原文链接
  python scripts/generate_thumbnails.py --use-abs       # 对 arxiv PDF 使用摘要页
  python scripts/generate_thumbnails.py --force         # 强制重新截图所有论文
"""

import argparse
import os
import re
import sys
from pathlib import Path
import yaml
from PIL import Image

# ---------- 路径配置 ----------
PAPERS_FILE = "data/papers.yml"
OUTPUT_DIR = "docs/assets/thumbnails"
# -----------------------------
VIEWPORT_WIDTH = 600
VIEWPORT_HEIGHT = 800
JPEG_QUALITY = 70          # 初始 JPEG 质量
MAX_SIZE_KB = 75          # 目标最大文件大小（KB）
TIMEOUT = 60_000
WAIT_AFTER_LOAD = 3000


def load_papers(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def save_papers(path: str, papers: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(papers, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def convert_pdf_to_abs(url: str) -> str:
    pattern = r'(https?://arxiv\.org)/pdf/(\d+\.\d+)(?:\.pdf)?'
    return re.sub(pattern, r'\1/abs/\2', url)


def sanitize_filename(name: str) -> str:
    return name.strip().replace("/", "_").replace("\\", "_")


def compress_image(input_path: str, max_kb: int) -> None:
    img = Image.open(input_path)
    quality = 70  # 起始质量更低，更快缩至目标
    while True:
        img.save(input_path, format="JPEG", quality=quality)
        if os.path.getsize(input_path) / 1024 <= max_kb or quality <= 5:
            break
        quality -= 10

    # 如果质量已降到极低仍超标，缩小尺寸
    if os.path.getsize(input_path) / 1024 > max_kb:
        w, h = img.size
        scale = 0.9
        while True:
            nw = max(1, int(w * scale))
            nh = max(1, int(h * scale))
            resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
            resized.save(input_path, format="JPEG", quality=60)
            if os.path.getsize(input_path) / 1024 <= max_kb or scale < 0.15:
                break
            scale -= 0.15


def update_thumbnail_field(papers: list, paper_id: str, thumbnail_path: str) -> bool:
    for paper in papers:
        if paper.get("id") == paper_id:
            paper["thumbnail"] = thumbnail_path
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="生成论文缩略图（轻量版）")
    parser.add_argument("--force", action="store_true", help="强制重新截图，覆盖已存在的缩略图")
    parser.add_argument("--use-abs", action="store_true", help="将 arxiv PDF 链接转换为摘要页再截图（默认直接使用原始链接）")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("请先安装 Playwright: pip install playwright && playwright install chromium")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    os.chdir(project_root)

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    papers_path = PAPERS_FILE
    if not os.path.isfile(papers_path):
        print(f"错误：找不到论文列表文件 {papers_path}")
        return

    papers = load_papers(papers_path)
    if not papers:
        print("错误：未能从 papers.yml 读取任何论文。")
        return

    print(f"共加载 {len(papers)} 篇论文\n")
    print(f"截图视口: {VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}, 目标体积 ≤ {MAX_SIZE_KB} KB")
    if args.use_abs:
        print("ℹ️  已启用 --use-abs，将对 arxiv PDF 使用摘要页截图。\n")

    fresh_screenshots = 0
    skipped_existing = 0
    yaml_updates = 0
    skipped_no_url = 0
    failed_screenshot = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/..."
        )

        for idx, paper in enumerate(papers, 1):
            paper_id = paper.get("id", f"unknown_{idx}")
            paper_url = paper.get("paper", "")

            if not paper_url:
                print(f"[{idx}/{len(papers)}] ⏭ 跳过 {paper_id}（无 paper URL）")
                skipped_no_url += 1
                continue

            output_name = sanitize_filename(paper_id) + ".jpg"
            output_path = os.path.join(OUTPUT_DIR, output_name)
            relative_path = os.path.join(OUTPUT_DIR, output_name).replace("\\", "/")

            if not args.force and os.path.isfile(output_path):
                current_thumb = paper.get("thumbnail", "")
                if current_thumb != relative_path:
                    update_thumbnail_field(papers, paper_id, relative_path)
                    yaml_updates += 1
                    print(f"[{idx}/{len(papers)}] 🔄 已修复 YAML → {relative_path}")
                else:
                    print(f"[{idx}/{len(papers)}] ⏭ 缩略图已存在，跳过 {paper_id}")
                skipped_existing += 1
                continue

            # 确定截图 URL
            screenshot_url = paper_url
            if args.use_abs:
                screenshot_url = convert_pdf_to_abs(paper_url)

            if args.use_abs and screenshot_url != paper_url:
                print(f"[{idx}/{len(papers)}] 🔄 使用摘要页: {paper_url}")

            print(f"[{idx}/{len(papers)}] 📷 正在截图 {paper_id}")

            page = context.new_page()
            success = False
            try:
                page.goto(screenshot_url, wait_until="networkidle", timeout=TIMEOUT)
                page.wait_for_timeout(WAIT_AFTER_LOAD)
                if screenshot_url.endswith(".pdf") or "/pdf/" in screenshot_url:
                    page.wait_for_timeout(2000)

                screenshot_bytes = page.screenshot(type="jpeg", quality=JPEG_QUALITY, full_page=False)
                with open(output_path, "wb") as f:
                    f.write(screenshot_bytes)
                compress_image(output_path, MAX_SIZE_KB)
                final_size = os.path.getsize(output_path) / 1024
                print(f"  ✅ 已保存: {output_path} ({final_size:.1f} KB)")
                success = True
            except Exception as e:
                print(f"  ❌ 截图失败: {e}")
                failed_screenshot += 1
            finally:
                page.close()

            if success:
                if update_thumbnail_field(papers, paper_id, relative_path):
                    yaml_updates += 1
                    print(f"  ✅ 已更新 thumbnail → {relative_path}")
                fresh_screenshots += 1

        browser.close()

    if yaml_updates > 0:
        save_papers(papers_path, papers)
        print(f"\n💾 已更新 {yaml_updates} 个 thumbnail 字段到 {papers_path}")

    print("\n" + "=" * 60)
    print("📊 执行完成！")
    print(f"   论文总数:        {len(papers)}")
    print(f"   新截图:          {fresh_screenshots}")
    print(f"   跳过（已存在）:  {skipped_existing}")
    print(f"   跳过（无 URL）:  {skipped_no_url}")
    print(f"   截图失败:        {failed_screenshot}")
    print(f"   YAML 字段更新:   {yaml_updates}")
    print("=" * 60)

    if not args.force:
        print("\n💡 提示：使用 --force 强制重新生成所有缩略图（会覆盖已有图片）")


if __name__ == "__main__":
    main()