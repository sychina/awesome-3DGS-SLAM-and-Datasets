#!/usr/bin/env python3
"""
自动为 3DGS-SLAM 论文生成缩略图（网页截图）。
新增功能：
  1. 自动将 arxiv PDF 链接替换为摘要页
  2. 截图成功后自动更新 papers.yml 中的 thumbnail 字段
  3. --force：强制重新截图，否则跳过已存在的缩略图
  4. 即使跳过截图，也会自动修复 YAML 中的 thumbnail 字段（svg → jpg）

用法：
  跳过已存在的，仅处理新论文：
    python scripts/generate_thumbnails.py
  强制重新截图所有论文：
    python scripts/generate_thumbnails.py --force
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path
from PIL import Image

# ---------- 路径配置（相对于项目根目录） ----------
PAPERS_FILE = "data/papers.yml"
OUTPUT_DIR = "docs/assets/thumbnails"
# -------------------------------------------------
VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 800
JPEG_QUALITY = 85
MAX_SIZE_KB = 400
TIMEOUT = 45_000          # 毫秒
WAIT_AFTER_LOAD = 2000    # 毫秒


def load_papers(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def save_papers(path: str, papers: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(papers, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def convert_pdf_to_abs(url: str) -> str:
    """将 arxiv PDF 链接替换为摘要页链接"""
    pattern = r'(https?://arxiv\.org)/pdf/(\d+\.\d+)(?:\.pdf)?'
    return re.sub(pattern, r'\1/abs/\2', url)


def sanitize_filename(name: str) -> str:
    return name.strip().replace("/", "_").replace("\\", "_")


def compress_image(input_path: str, max_kb: int) -> None:
    img = Image.open(input_path)
    quality = 90
    while True:
        img.save(input_path, format="JPEG", quality=quality)
        if os.path.getsize(input_path) / 1024 <= max_kb or quality <= 10:
            break
        quality -= 5

    if os.path.getsize(input_path) / 1024 > max_kb:
        width, height = img.size
        scale = 0.9
        while True:
            new_w = int(width * scale)
            new_h = int(height * scale)
            resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            resized.save(input_path, format="JPEG", quality=75)
            if os.path.getsize(input_path) / 1024 <= max_kb or scale < 0.2:
                break
            scale -= 0.1


def update_thumbnail_field(papers: list, paper_id: str, thumbnail_path: str) -> bool:
    """更新 papers 列表中指定论文的 thumbnail 字段"""
    for paper in papers:
        if paper.get("id") == paper_id:
            paper["thumbnail"] = thumbnail_path
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="生成论文缩略图")
    parser.add_argument("--force", action="store_true",
                        help="强制重新截图，覆盖已有缩略图")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("请先安装 Playwright: pip install playwright && playwright install chromium")
        sys.exit(1)

    # 切换到项目根目录
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

    # 统计
    fresh_screenshots = 0      # 新截图
    skipped_existing = 0       # 已存在，跳过截图
    yaml_updates = 0           # 更新了 thumbnail 字段
    skipped_no_url = 0
    failed_screenshot = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent="Mozilla/5.0 ..."
        )

        for idx, paper in enumerate(papers, 1):
            paper_id = paper.get("id", f"unknown_{idx}")
            paper_url = paper.get("paper", "")

            if not paper_url:
                print(f"[{idx}/{len(papers)}] ⏭ 跳过 {paper_id}（无 paper URL）")
                skipped_no_url += 1
                # 即使没有 URL，如果已有 jpg 文件，也可以修正 YAML
                # 但这里我们保持原样，因为无法确定正确的快照
                continue

            # 目标文件路径
            output_name = sanitize_filename(paper_id) + ".jpg"
            output_path = os.path.join(OUTPUT_DIR, output_name)
            relative_path = os.path.join(OUTPUT_DIR, output_name).replace("\\", "/")

            # 检查是否已存在
            file_exists = os.path.isfile(output_path)

            # 决定是否需要截图
            need_screenshot = not file_exists or args.force

            if not need_screenshot:
                # 跳过截图，但检查 YAML 字段是否需要修正
                current_thumb = paper.get("thumbnail", "")
                if current_thumb != relative_path:
                    # 更新 YAML
                    update_thumbnail_field(papers, paper_id, relative_path)
                    yaml_updates += 1
                    print(f"[{idx}/{len(papers)}] 🔄 已修复 YAML 字段 → {relative_path}")
                else:
                    print(f"[{idx}/{len(papers)}] ⏭ 缩略图已存在，跳过 {paper_id}")
                skipped_existing += 1
                continue

            # --- 需要截图 ---
            screenshot_url = convert_pdf_to_abs(paper_url)
            if screenshot_url != paper_url:
                print(f"[{idx}/{len(papers)}] 🔄 PDF → 摘要页: {paper_url}")

            print(f"[{idx}/{len(papers)}] 📷 正在截图 {paper_id}")

            page = context.new_page()
            success = False
            try:
                page.goto(screenshot_url, wait_until="networkidle", timeout=TIMEOUT)
                page.wait_for_timeout(WAIT_AFTER_LOAD)
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
                # 更新 YAML 字段
                if update_thumbnail_field(papers, paper_id, relative_path):
                    yaml_updates += 1
                    print(f"  ✅ 已更新 thumbnail → {relative_path}")
                fresh_screenshots += 1

        browser.close()

    # 写回 YAML
    if yaml_updates > 0:
        save_papers(papers_path, papers)
        print(f"\n💾 已更新 {yaml_updates} 个 thumbnail 字段到 {papers_path}")

    # 总结
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
        print("\n💡 提示：若要强制重新生成所有缩略图，请使用 --force")


if __name__ == "__main__":
    main()