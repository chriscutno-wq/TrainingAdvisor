"""Convert data/training_catalog.xlsx -> data/catalog.json (deduped, cleaned)."""
import json, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TYPE = {"Courses": "Course", "Webinars": "Webinar", "Sessions": "Live session"}
# Descriptions in the source were copied from unrelated courses; index these by title only.
TITLE_ONLY = {"Using the SDK", "Application of the SDK"}

df = pd.read_excel(ROOT / "data" / "training_catalog.xlsx")
items, order = {}, []
for _, r in df.iterrows():
    title = str(r["Course Title"]).strip()
    typ = TYPE[r["Course Type"]]
    url = str(r["Course URL"]).strip()
    cat = str(r["Category"]).strip()
    desc = str(r["Description"]).strip().replace("\r", "")
    key = (title, typ, url)
    if key in items:                      # exact duplicate row -> merge categories
        if cat not in items[key]["cats"]:
            items[key]["cats"].append(cat)
        continue
    if '" with "' in desc:                # stray duplicated paragraph in source
        desc = desc.split('" with "')[0].strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", desc) if p.strip()]
    notes = [re.sub(r"^note:\s*", "", p, flags=re.I) for p in paras if p.lower().startswith("note:")]
    main = [p for p in paras if not p.lower().startswith("note:")]
    text = " ".join(main)
    dur = None
    m = re.search(r"(\d+)[- ]minute", text)
    if m:
        dur = f"{m.group(1)} min"
    else:
        m = re.search(r"(\d+(?:\.\d+)?)\s*hours?\b", text)
        if m:
            dur = f"{m.group(1)} hour" + ("" if m.group(1) == "1" else "s")
    items[key] = dict(id=len(order), title=title, type=typ, cats=[cat], url=url,
                      desc=main, notes=notes, dur=dur, titleOnly=title in TITLE_ONLY)
    order.append(key)

data = [items[k] for k in order]
(ROOT / "data" / "catalog.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(data)} unique resources from {len(df)} rows -> data/catalog.json")
