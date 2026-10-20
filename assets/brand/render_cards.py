"""Render the link-preview cards (1200x630) from their HTML masters with Playwright + Edge.

    python assets/brand/render_cards.py            # social.png and invite.png
    python assets/brand/render_cards.py invite     # one card

Same approach as IIT-APP marketing/social/render.py. Numbers in the masters come from the content
database (docs/08 section 8), never from memory.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CARDS = {"social": "make_social.html", "invite": "make_invite.html"}

which = sys.argv[1:] or list(CARDS)
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--allow-file-access-from-files"])
    page = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    for name in which:
        page.goto((HERE / CARDS[name]).as_uri())
        page.wait_for_timeout(400)  # font
        out = HERE / f"{name}.png"
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        print("wrote", out, out.stat().st_size, "bytes")
    b.close()
