"""Search relevance smoke tests. Requires: pip install playwright && playwright install chromium
Run: python tests/search_test.py   (build first: python scripts/build.py)"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parent.parent / "dist" / "training-advisor.html").as_uri()

# query -> title that must be the #1 result (None = must return nothing)
CASES = {
    "client can't reset their password": "Effortless User Registration & Identity Verification in the Admin Console",
    "set up Zelle": "Zelle: Features & Functionality",
    "business wire transfers": "Business Wire Transfers Essentials: How to Customize, Process, and Support Wire Transfers",
    "mobile check deposit": "Remote Deposit Capture (RDC): Depositing Checks Electronically",
    "push notifications": "Airship and Gimbal Messaging: Registration, Setup, and Targeting Users",
    "change our logo": "Customizing Your Theme With Theme Builder",
    "skip a payment": "Skip a Payment",
    "view as user": "Using the View as User Feature",
    "chat": "Chat: Features & Integrations",
    "overview of the platform": "Alkami Platform Overview",
    "xyzzy": None,
}

fails = 0
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(PAGE, wait_until="domcontentloaded")
    for q, want in CASES.items():
        res = pg.evaluate("q => window.__advisor.search(q)", q)
        got = res[0][0] if res else None
        ok = got == want
        fails += not ok
        print(("PASS" if ok else "FAIL"), "|", q, "->", got)
    b.close()
if errs:
    print("JS errors:", errs); fails += 1
sys.exit(1 if fails else 0)
