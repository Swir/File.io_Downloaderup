#!/usr/bin/env python3
"""Generate/check SWIR Progress SVG PRO assets for this repository."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "readme"
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

EXPECTED = {"progress-card.svg": CARD, "progress-mini.svg": MINI}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if committed SVG output is stale")
    args = parser.parse_args()
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, content in EXPECTED.items():
        path = ASSET_DIR / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        print("stale progress assets: " + ", ".join(stale))
        return 1
    print(f"{PROJECT}: N/A — {SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
