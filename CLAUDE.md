# Training Advisor

Single-file web app that helps customer service reps find the right Alkami training
(course / webinar / live session) for a client's question. Users type a need or issue,
the app searches the catalog and recommends resources.

## Hard rules
- **Content comes only from `data/training_catalog.xlsx`.** Never invent, paraphrase, or add
  course info. Related-term lists (the `SYN_RAW` array) may widen *matching* only.
- **Follow the brand guidelines** in `brand/Alkami_Brand_Guidelines_2025.pdf` (summary below).
- Output must stay a **single self-contained HTML file** (CSS/JS/data/logo inlined).
  Only external requests allowed: Google Fonts (Nunito Sans). No other network calls, no backend.

## Layout
- `src/template.html` – the whole app (CSS, markup, search engine, UI). Placeholders: `__DATA__`, `__LOGO_D__`.
- `src/logo-path.txt` – official Alkami logo vector path, extracted from the brand PDF. **Never redraw or edit it.**
- `data/training_catalog.xlsx` – source of truth. `data/catalog.json` is generated.
- `scripts/build_catalog.py` – xlsx -> catalog.json (dedupes, merges categories, splits "Note:" callouts, parses durations).
- `scripts/build.py` – template + catalog + logo -> `dist/training-advisor.html`.
- `tests/search_test.py` – Playwright relevance checks (`window.__advisor.search(q)`).

## Workflow
```
pip install pandas openpyxl
python scripts/build_catalog.py   # when the spreadsheet changes
python scripts/build.py           # always, after any change
python tests/search_test.py       # optional: pip install playwright && playwright install chromium
```
Open `dist/training-advisor.html` in a browser to check. Test at 390px wide, and in light + dark mode.

## Brand cheat sheet
- Navy `#071351` is the hero. Tints: `#152E7C #0251B3 #1F64C5 #357DE4`. Neutrals: `#FFFFFF #FAFAFA #EFEFEF #DBDBDB`.
- Gold `#F3AB39 → #FAD564` is an **accent only**, used sparingly. Never a primary color.
- Secondary: teal `#1B9587 #1EAF9B #26C4AA #29DBBE`, purple `#692E53 #773E64 #914475 #AE5294`, light blue `#50C1EC #67CFEE #7EDEFC #92EAFF`.
- Type: **Alverata** bold/semibold for headlines (fallback Cambria), **Nunito Sans** regular for body (fallback Calibri).
- Logo: never modify, recolor, or stretch. Keep clear space ≈ half the width of the "A". Gold logo only on navy/dark; use one-color navy/white elsewhere.
- Glyphs: geometric shapes on a grid, mainly two-tone, purposeful. Icons are line icons only.
- Voice: Intentional, Proficient, Honest, Helpful, Plucky. Be concise, confident, skip jargon and chest-pounding.

## Known catalog data issues (flag, don't silently fix in the app)
- 8 exact-duplicate rows (merged by build_catalog.py).
- "Using the SDK" / "Application of the SDK" have descriptions copied from unrelated courses -> indexed by title only (`TITLE_ONLY`).
- "Executing Bulk User Operations" and "Chat: Features & Integrations" share one URL – probably a source error.
