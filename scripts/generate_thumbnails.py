#!/usr/bin/env python3
"""
自动为 3DGS-SLAM 论文生成缩略图（网页截图）。
适配目录结构：
  data/           - 存放 papers.yml
  docs/assets/thumbnails/ - 输出缩略图（JPEG，≤400KB）
  scripts/        - 本脚本所在位置

用法：在项目根目录执行：
  python scripts/generate_thumbnails.py
"""

import os
import sys
import yaml
import time
from pathlib import Path
from PIL import Image

# ---------- 路径配置（相对于项目根目录） ----------
PAPERS_FILE = "data/papers.yml"             # 论文列表
OUTPUT_DIR = "docs/assets/thumbnails"       # 缩略图输出目录
# -------------------------------------------------
VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 800
JPEG_QUALITY = 85
MAX_SIZE_KB = 400
TIMEOUT = 45_000          # 毫秒
WAIT_AFTER_LOAD = 2000    # 毫秒

def load_papers(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data else []

def sanitize_filename(name: str) -> str:
    return name.strip().replace("/", "_").replace("\\", "_")

def compress_image(input_path: str, max_kb: int) -> None:
    img = Image.open(input_path)
    quality = 90
    while True:
        img.save(input_path, format="JPEG", quality=quality)
        size_kb = os.path.getsize(input_path) / 1024
        if size_kb <= max_kb or quality <= 10:
            break
        quality -= 5

    if os.path.getsize(input_path) / 1024 > max_kb:
        width, height = img.size
        scale = 0.9
        while True:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            resized.save(input_path, format="JPEG", quality=75)
            if os.path.getsize(input_path) / 1024 <= max_kb or scale < 0.2:
                break
            scale -= 0.1

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("请先安装 Playwright: pip install playwright && playwright install chromium")
        sys.exit(1)

    # 切换到项目根目录（假设脚本在 scripts/ 下）
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

    print(f"共加载 {len(papers)} 篇论文，开始截图...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/... Chrome/..."
        )

        for idx, paper in enumerate(papers, 1):
            paper_id = paper.get("id", f"unknown_{idx}")
            paper_url = paper.get("paper", "")
            if not paper_url:
                print(f"[{idx}/{len(papers)}] 跳过 {paper_id}（无 paper URL）")
                continue

            print(f"[{idx}/{len(papers)}] 正在处理 {paper_id} -> {paper_url}")
            output_name = sanitize_filename(paper_id) + ".jpg"
            output_path = os.path.join(OUTPUT_DIR, output_name)

            page = context.new_page()
            try:
                page.goto(paper_url, wait_until="networkidle", timeout=TIMEOUT)
                page.wait_for_timeout(WAIT_AFTER_LOAD)
                screenshot_bytes = page.screenshot(type="jpeg", quality=JPEG_QUALITY, full_page=False)
                with open(output_path, "wb") as f:
                    f.write(screenshot_bytes)
                compress_image(output_path, MAX_SIZE_KB)
                final_size = os.path.getsize(output_path) / 1024
                print(f"  ✅ 已保存: {output_path} ({final_size:.1f} KB)")
            except Exception as e:
                print(f"  ❌ 截图失败: {e}")
            finally:
                page.close()

        browser.close()

    print("完成！")

if __name__ == "__main__":
    main()