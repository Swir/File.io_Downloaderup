#!/usr/bin/env python3
"""Generate/check SWIR Progress SVG PRO assets for this repository."""
from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "readme"
README = ROOT / "README.md"
PROJECT = "File.io Transfer CLI"
SCOPE = "product roadmap"
SOURCE = "No authoritative measurable roadmap file exists in this repository"

CARD = """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"180\" viewBox=\"0 0 1200 180\" role=\"img\" aria-labelledby=\"title desc\">
  <title id=\"title\">File.io Transfer CLI product progress</title>
  <desc id=\"desc\">Product progress is not available because the repository has no authoritative measurable roadmap.</desc>
  <defs><linearGradient id=\"bg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop stop-color=\"#02050A\"/><stop offset=\"1\" stop-color=\"#07111C\"/></linearGradient><pattern id=\"grid\" width=\"28\" height=\"28\" patternUnits=\"userSpaceOnUse\"><path d=\"M28 0H0V28\" fill=\"none\" stroke=\"#62E5FF\" stroke-opacity=\".05\"/></pattern></defs>
  <rect x=\"1\" y=\"1\" width=\"1198\" height=\"178\" rx=\"24\" fill=\"url(#bg)\" stroke=\"#62E5FF\" stroke-opacity=\".22\"/><rect x=\"1\" y=\"1\" width=\"1198\" height=\"178\" rx=\"24\" fill=\"url(#grid)\"/>
  <text x=\"50\" y=\"45\" fill=\"#62E5FF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"17\" font-weight=\"700\" letter-spacing=\"3\">SWIR PROGRESS</text>
  <text x=\"50\" y=\"80\" fill=\"#F4FAFF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"30\" font-weight=\"800\">File.io Transfer CLI</text>
  <text x=\"50\" y=\"108\" fill=\"#8DA8B8\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"15\">Scope: product roadmap</text>
  <text x=\"1080\" y=\"80\" text-anchor=\"end\" fill=\"#F4FAFF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"34\" font-weight=\"800\">N/A</text>
  <text x=\"1080\" y=\"108\" text-anchor=\"end\" fill=\"#62E5FF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"14\" font-weight=\"700\" letter-spacing=\"1\">ROADMAP NOT DEFINED</text>
  <rect x=\"50\" y=\"126\" width=\"1100\" height=\"22\" rx=\"11\" fill=\"#08131F\" stroke=\"#62E5FF\" stroke-opacity=\".14\"/>
  <text x=\"50\" y=\"168\" fill=\"#8DA8B8\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"13\">No authoritative measurable roadmap is present in this repository.</text>
</svg>
"""

MINI = """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"900\" height=\"72\" viewBox=\"0 0 900 72\" role=\"img\" aria-labelledby=\"title desc\">
  <title id=\"title\">File.io Transfer CLI roadmap progress</title><desc id=\"desc\">Roadmap progress is N/A because no authoritative measurable roadmap exists.</desc>
  <rect x=\"1\" y=\"1\" width=\"898\" height=\"70\" rx=\"18\" fill=\"#02050A\" stroke=\"#62E5FF\" stroke-opacity=\".22\"/>
  <text x=\"24\" y=\"28\" fill=\"#62E5FF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"13\" font-weight=\"700\" letter-spacing=\"2\">PRODUCT ROADMAP</text>
  <text x=\"24\" y=\"53\" fill=\"#F4FAFF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"20\" font-weight=\"800\">N/A</text>
  <rect x=\"170\" y=\"24\" width=\"700\" height=\"20\" rx=\"10\" fill=\"#08131F\"/>
  <text x=\"870\" y=\"58\" text-anchor=\"end\" fill=\"#8DA8B8\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"12\">No measurable roadmap</text>
</svg>
"""

TEMPLATE = """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"180\" viewBox=\"0 0 1200 180\" role=\"img\" aria-labelledby=\"title desc\">
  <title id=\"title\">SWIR progress template</title><desc id=\"desc\">TEMPLATE / NOT PROJECT DATA. Reusable local progress card template.</desc>
  <defs><linearGradient id=\"bg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop stop-color=\"#02050A\"/><stop offset=\"1\" stop-color=\"#07111C\"/></linearGradient><linearGradient id=\"fill\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\"><stop stop-color=\"#0088FF\"/><stop offset=\"1\" stop-color=\"#62E5FF\"/></linearGradient></defs>
  <rect x=\"1\" y=\"1\" width=\"1198\" height=\"178\" rx=\"24\" fill=\"url(#bg)\" stroke=\"#62E5FF\" stroke-opacity=\".22\"/>
  <text x=\"50\" y=\"48\" fill=\"#62E5FF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"18\" font-weight=\"700\" letter-spacing=\"4\">TEMPLATE / NOT PROJECT DATA</text>
  <text x=\"50\" y=\"84\" fill=\"#F4FAFF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"30\" font-weight=\"800\">PROJECT / SCOPE</text>
  <text x=\"1080\" y=\"84\" text-anchor=\"end\" fill=\"#F4FAFF\" font-family=\"Segoe UI,Arial,sans-serif\" font-size=\"34\" font-weight=\"800\">XX.X%</text>
  <rect x=\"50\" y=\"126\" width=\"1100\" height=\"22\" rx=\"11\" fill=\"#08131F\"/><rect x=\"50\" y=\"126\" width=\"550\" height=\"22\" rx=\"11\" fill=\"url(#fill)\"/>
</svg>
"""

EXPECTED = {
    "progress-card.svg": CARD,
    "progress-mini.svg": MINI,
    "progress-template.svg": TEMPLATE,
}
LEGACY_METER = re.compile(r"[█▓▒░▰▱■□]{4,}|\[[#=]{6,}[#=\- ]*\]")


def validate_presentation() -> list[str]:
    errors: list[str] = []
    for name, content in EXPECTED.items():
        try:
            ET.fromstring(content)
        except ET.ParseError as exc:
            errors.append(f"invalid SVG {name}: {exc}")
    readme = README.read_text(encoding="utf-8")
    for required in (
        "<!-- SWIR-README-STANDARD:v2 -->",
        "assets/readme/progress-card.svg",
        "assets/readme/progress-mini.svg",
        "## 🔎 Search Keywords",
    ):
        if required not in readme:
            errors.append(f"README missing required marker: {required}")
    if LEGACY_METER.search(readme):
        errors.append("README contains a retired character progress meter")
    if "TEMPLATE / NOT PROJECT DATA" not in TEMPLATE:
        errors.append("progress template is not clearly labelled")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if committed SVG output or README presentation is stale")
    args = parser.parse_args()
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    errors = validate_presentation()
    stale = []
    for name, content in EXPECTED.items():
        path = ASSET_DIR / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        errors.append("stale progress assets: " + ", ".join(stale))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"{PROJECT}: N/A — {SOURCE}; SVG-only presentation verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
