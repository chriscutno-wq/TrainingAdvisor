"""Inline catalog + logo into src/template.html -> dist/training-advisor.html (single self-contained file)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
data = json.dumps(json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8")),
                  ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
logo = (ROOT / "src" / "logo-path.txt").read_text().strip()
out = tpl.replace("__DATA__", data).replace("__LOGO_D__", logo)
(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist" / "training-advisor.html").write_text(out, encoding="utf-8")
print(f"dist/training-advisor.html  ({len(out)/1024:.0f} KB)")
