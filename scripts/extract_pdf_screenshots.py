#!/usr/bin/env python3
"""Extract embedded images from archive PDFs into docs/screenshots/."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "canvas-submissions"
OUT = ROOT / "docs" / "screenshots"


def slug(name: str) -> str:
    s = name.removesuffix(".pdf").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:48]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(ARCHIVE.glob("*.pdf")):
        reader = PdfReader(pdf)
        base = slug(pdf.name)
        count = 0
        for pi, page in enumerate(reader.pages, start=1):
            for ii, img in enumerate(page.images, start=1):
                ext = ".png" if img.name.lower().endswith(".png") else ".jpg"
                dest = OUT / f"{base}-p{pi}-img{ii}{ext}"
                dest.write_bytes(img.data)
                count += 1
        print(f"{pdf.name}: {count} images")


if __name__ == "__main__":
    main()
