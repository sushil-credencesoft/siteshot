# crawl logic placeholder (use earlier provided crawl code here)
#!/usr/bin/env python3
"""
SITE_SHOT — Production-grade Website Visual Crawler
===================================================

PURPOSE
-------
Create a deterministic, auditable, visual snapshot of an entire website
for QA, regression detection, UX audits, and CI pipelines.

SETUP
-----
pip install playwright aiohttp lxml
playwright install

EXAMPLES
--------
python site_shot.py --start-url https://example.com
python site_shot.py --start-url https://example.com --sitemap https://example.com/sitemap.xml
python site_shot.py --start-url https://example.com --nav-selector "header nav a"
"""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import time
from collections import deque
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse, urlunparse

import aiohttp
from lxml import html, etree
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError


# ============================================================
# Core Utilities
# ============================================================

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_filename(text: str, max_len: int = 120) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-]", "", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:max_len] if text else "page"


def parse_viewport(value: str):
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except Exception:
        raise argparse.ArgumentTypeError("Viewport must be WIDTHxHEIGHT")


def normalize_url(
    url: str,
    base: Optional[str] = None,
    include_query: bool = False
) -> Optional[str]:
    try:
        if base:
            url = urljoin(base, url)
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return None

        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        query = parsed.query if include_query else ""
        return urlunparse((parsed.scheme, parsed.netloc, path, "", query, ""))
    except Exception:
        return None


def same_origin(a: str, b: str) -> bool:
    return urlparse(a).netloc == urlparse(b).netloc


# ============================================================
# Network helpers
# ============================================================

async def fetch_text(session, url: str, timeout: int) -> Optional[str]:
    try:
        async with session.get(url, timeout=timeout) as r:
            if r.status == 200:
                return await r.text()
    except Exception:
        return None
    return None


async def load_sitemap(session, url: str, timeout: int) -> List[str]:
    xml = await fetch_text(session, url, timeout)
    if not xml:
        return []
    urls = []
    try:
        root = etree.fromstring(xml.encode())
        for loc in root.findall(".//{*}loc"):
            urls.append(loc.text.strip())
    except Exception:
        pass
    return urls


# ============================================================
# Playwright logic
# ============================================================

async def wait_ready(page, selector: Optional[str], timeout_ms: int):
    await page.wait_for_load_state("networkidle", timeout=timeout_ms)
    if selector:
        await page.wait_for_selector(selector, timeout=timeout_ms)


async def page_name(page, url: str) -> str:
    try:
        h1 = await page.eval_on_selector(
            "h1", "el => el && el.offsetParent ? el.innerText : null"
        )
        if h1:
            return h1.strip()
    except Exception:
        pass

    try:
        title = await page.title()
        if title:
            return title.strip()
    except Exception:
        pass

    return urlparse(url).path.strip("/").split("/")[-1] or "home"


async def capture(
    index: int,
    page,
    url: str,
    out_dir: str,
    ready_selector: Optional[str],
    timeout_ms: int
) -> Dict:
    record = {
        "url": url,
        "page_name": None,
        "title": None,
        "screenshot_file": None,
        "status": "fail",
        "error": None,
        "captured_at": utc_now()
    }

    try:
        await page.goto(url, timeout=timeout_ms)
        await wait_ready(page, ready_selector, timeout_ms)

        name = await page_name(page, url)
        title = await page.title()

        filename = f"{index:03d}-{safe_filename(name)}.png"
        path = os.path.join(out_dir, filename)

        await page.screenshot(path=path, full_page=True)

        record.update(
            page_name=name,
            title=title,
            screenshot_file=os.path.join("screenshots", filename),
            status="success"
        )

    except PWTimeoutError:
        record["error"] = "Timeout waiting for page readiness"
    except Exception as e:
        record["error"] = str(e)

    return record


async def extract_links(page, base_url: str) -> List[str]:
    links = []
    try:
        doc = html.fromstring(await page.content())
        for a in doc.xpath("//a[@href]"):
            href = a.get("href")
            if href and not href.startswith(("mailto:", "tel:", "javascript:")):
                links.append(href)
    except Exception:
        pass
    return links


# ============================================================
# Main Runner
# ============================================================

async def run(args):
    start_time = time.time()

    os.makedirs(args.out_dir, exist_ok=True)
    shots_dir = os.path.join(args.out_dir, "screenshots")
    os.makedirs(shots_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(args.out_dir, "run.log"))
        ],
    )

    viewport = parse_viewport(args.viewport)
    timeout_ms = args.timeout * 1000

    visited: Set[str] = set()
    queue = deque()

    async with aiohttp.ClientSession() as session:
        if args.sitemap:
            urls = await load_sitemap(session, args.sitemap, args.timeout)
            for u in urls:
                queue.append(normalize_url(u))
        else:
            queue.append(normalize_url(args.start_url))

    manifest = []
    index = 1

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            user_agent=args.user_agent,
            is_mobile=args.mobile
        )

        while queue and index <= args.max_pages:
            url = queue.popleft()
            if not url or url in visited:
                continue
            if not same_origin(url, args.start_url):
                continue

            visited.add(url)
            page = await context.new_page()

            result = await capture(
                index, page, url, shots_dir,
                args.ready_selector, timeout_ms
            )
            await page.close()

            manifest.append(result)
            logging.info(f"[{index}] {url} -> {result['status']}")
            index += 1

            if not args.sitemap:
                page = await context.new_page()
                try:
                    await page.goto(url, timeout=timeout_ms)
                    for href in await extract_links(page, url):
                        norm = normalize_url(href, url)
                        if norm and norm not in visited:
                            queue.append(norm)
                except Exception:
                    pass
                await page.close()

        await browser.close()

    with open(os.path.join(args.out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    logging.info(
        f"FINISHED | total={len(manifest)} "
        f"success={sum(m['status']=='success' for m in manifest)} "
        f"failed={sum(m['status']=='fail' for m in manifest)} "
        f"elapsed={round(time.time()-start_time,2)}s"
    )


def main():
    p = argparse.ArgumentParser("SITE_SHOT — QA Visual Crawler")
    p.add_argument("--start-url", required=True)
    p.add_argument("--out-dir", default="output")
    p.add_argument("--max-pages", type=int, default=100)
    p.add_argument("--sitemap")
    p.add_argument("--nav-selector")
    p.add_argument("--ready-selector")
    p.add_argument("--viewport", default="1440x900")
    p.add_argument("--timeout", type=int, default=45)
    p.add_argument("--user-agent")
    p.add_argument("--mobile", action="store_true")

    asyncio.run(run(p.parse_args()))


if __name__ == "__main__":
    main()
