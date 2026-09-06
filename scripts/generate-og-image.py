#!/usr/bin/env python3
"""Generate static/og.png from the homepage copy so the share card never drifts.

The card mirrors the homepage: site name, the h1, the intro paragraph, and the
canonical host. All four strings are read out of index.html, so editing the site
copy and rerunning this script is the only supported way to change the image.

Rendering uses headless Chrome with the site's own palette and font stack, which
is why the output matches the rest of the site on macOS (-apple-system -> SF Pro).

    python3 scripts/generate-og-image.py

When the bytes change, every `static/og.png?v=N` reference in the HTML is bumped
to N+1 so CDN and social-scraper caches fetch the new image.
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOMEPAGE = ROOT / "index.html"
OUTPUT = ROOT / "static" / "og.png"

WIDTH = 1200
HEIGHT = 630
RENDER_TIMEOUT = 90

# Palette and type stack copied from the :root block in styles.css.
BACKGROUND = "#fcfcfb"
FOREGROUND = "#2c2826"
SOFT = "color-mix(in srgb, #2c2826 86%, #fcfcfb)"
MUTED = "color-mix(in srgb, #2c2826 75%, #fcfcfb)"
SUBTLE = "color-mix(in srgb, #2c2826 64%, #fcfcfb)"
FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'

CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)


def find_chrome() -> str:
    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    for path in CHROME_CANDIDATES:
        if Path(path).is_file():
            return path
    sys.exit("no Chrome/Chromium binary found; install Chrome to render the card")


def text_of(markup: str) -> str:
    """Strip inline tags, decode entities, collapse whitespace."""
    stripped = re.sub(r"<[^>]+>", "", markup)
    return re.sub(r"\s+", " ", html.unescape(stripped).replace("\u00a0", " ")).strip()


def capture(pattern: str, source: str, label: str) -> str:
    match = re.search(pattern, source, re.DOTALL)
    if not match:
        sys.exit(f"could not read the {label} out of {HOMEPAGE.name}")
    return text_of(match.group(1))


def read_copy() -> dict[str, str]:
    source = HOMEPAGE.read_text(encoding="utf-8")
    canonical = capture(
        r'<link rel="canonical" href="([^"]+)"', source, "canonical URL"
    )
    host = canonical.split("//", 1)[-1].strip("/")
    return {
        "eyebrow": capture(
            r'<meta property="og:site_name" content="([^"]+)"', source, "site name"
        ),
        "headline": capture(
            r'<h1 id="home-heading">(.*?)</h1>', source, "homepage h1"
        ),
        "lead": capture(
            r'<p class="intro-copy">(.*?)</p>', source, "intro paragraph"
        ),
        # The card prints the bare domain even though the canonical host is www.
        "domain": host.removeprefix("www."),
    }


def build_document(copy: dict[str, str]) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <style>
      html, body {{ margin: 0; padding: 0; }}
      body {{
        width: {WIDTH}px;
        height: {HEIGHT}px;
        padding: 112px 96px 90px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        background: {BACKGROUND};
        color: {FOREGROUND};
        font-family: {FONT};
        font-synthesis: none;
        -webkit-font-smoothing: antialiased;
      }}
      p {{ margin: 0; }}
      .eyebrow {{
        font-size: 26px;
        font-weight: 500;
        line-height: 1;
        color: {SOFT};
      }}
      h1 {{
        margin: 51px 0 0;
        font-size: 61px;
        font-weight: 600;
        line-height: 1.164;
        letter-spacing: -0.02em;
      }}
      .lead {{
        margin: 26px 0 0;
        max-width: 900px;
        font-size: 31px;
        font-weight: 400;
        line-height: 1.484;
        color: {MUTED};
        text-wrap: balance;
      }}
      .domain {{
        margin-top: auto;
        font-size: 26px;
        line-height: 1;
        color: {SUBTLE};
      }}
    </style>
  </head>
  <body>
    <p class="eyebrow">{html.escape(copy["eyebrow"])}</p>
    <h1>{html.escape(copy["headline"])}</h1>
    <p class="lead">{html.escape(copy["lead"])}</p>
    <p class="domain">{html.escape(copy["domain"])}</p>
  </body>
</html>
"""


def render(document: str) -> bytes:
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as workdir:
        work = Path(workdir)
        page = work / "card.html"
        page.write_text(document, encoding="utf-8")
        shot = work / "og.png"
        log = work / "chrome.log"
        # Chrome writes the screenshot and then keeps running (and its updater
        # outlives the browser), so its output goes to a file rather than an
        # inherited pipe, and the process is stopped once the image settles.
        with log.open("wb") as sink:
            browser = subprocess.Popen(
                [
                    chrome,
                    "--headless=new",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    "--virtual-time-budget=2000",
                    f"--window-size={WIDTH},{HEIGHT}",
                    f"--screenshot={shot}",
                    f"--user-data-dir={work / 'profile'}",
                    "--no-first-run",
                    "--no-default-browser-check",
                    page.as_uri(),
                ],
                stdout=sink,
                stderr=subprocess.STDOUT,
            )
            try:
                deadline = time.monotonic() + RENDER_TIMEOUT
                settled = -1
                while time.monotonic() < deadline:
                    if browser.poll() is not None:
                        break
                    size = shot.stat().st_size if shot.is_file() else 0
                    if size and size == settled:
                        break
                    settled = size
                    time.sleep(0.25)
            finally:
                if browser.poll() is None:
                    browser.terminate()
                    try:
                        browser.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        browser.kill()
        if not shot.is_file():
            tail = log.read_text(encoding="utf-8", errors="replace").strip()[-2000:]
            sys.exit(f"chrome failed to render the card:\n{tail}")
        return shot.read_bytes()


def bump_cache_version() -> int | None:
    """Advance every `static/og.png?v=N` reference; returns the new version."""
    pattern = re.compile(r"(static/og\.png\?v=)(\d+)")
    pages = sorted(ROOT.glob("**/*.html"))
    versions = {
        int(match.group(2))
        for page in pages
        for match in pattern.finditer(page.read_text(encoding="utf-8"))
    }
    if not versions:
        return None
    new_version = max(versions) + 1
    for page in pages:
        source = page.read_text(encoding="utf-8")
        updated = pattern.sub(rf"\g<1>{new_version}", source)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
    return new_version


def main() -> None:
    copy = read_copy()
    for label in ("eyebrow", "headline", "lead", "domain"):
        print(f"{label:9} {copy[label]}")

    image = render(build_document(copy))
    if OUTPUT.is_file() and OUTPUT.read_bytes() == image:
        print(f"\n{OUTPUT.relative_to(ROOT)} already current ({len(image)} bytes)")
        return

    OUTPUT.write_bytes(image)
    version = bump_cache_version()
    print(f"\nwrote {OUTPUT.relative_to(ROOT)} ({len(image)} bytes)")
    if version is not None:
        print(f"bumped share-image references to static/og.png?v={version}")


if __name__ == "__main__":
    main()
