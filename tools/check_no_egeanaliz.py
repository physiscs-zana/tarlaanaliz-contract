#!/usr/bin/env python3
"""
Brand guard: ensures the sibling brand "EgeAnaliz" never leaks into this repo.

tarlaanaliz-contracts is periodically synced from egeanaliz-contracts (which is a
rebranded, more-advanced sibling). This guard prevents the egeanaliz brand from
slipping back in during a sync.

Checks (case-insensitive):
  1. File and directory names containing the contiguous brand "egeanaliz".
  2. File contents containing the contiguous brand "egeanaliz".

Does NOT match the Turkish phrase "ege analizi" (two whitespace-separated words),
which is legitimate domain language.

Exits 1 on any hit, 0 if clean.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Contiguous brand form only. Assembled from parts so this guard's own source
# does not contain the literal brand and self-match. The negative lookbehind
# lets legitimate references to THIS tool's own name (check_no_egeanaliz) pass —
# only the bare brand is a violation.
_FOREIGN_BRAND = "ege" + "analiz"
BRAND_RE = re.compile(r"(?<!check_no_)" + _FOREIGN_BRAND, re.IGNORECASE)

# Aegean (sibling-region) leakage that the bare-brand regex misses: Aegean place
# names and `ege-`/`ege_` dataset/model id prefixes — these are high-signal leaks
# (they appeared in ported example payloads) and do not occur in legitimate text.
# NOTE: bare "aegean"/"tariş"/"ege"/"EGE" are intentionally NOT flagged — they
# legitimately appear in exclusion documentation (CHANGELOG, enum notes, tests)
# describing what was deliberately left out, and would cause false positives.
REGION_RE = re.compile(
    r"ala[şs]ehir|\bizmir\b|\bmanisa\b|\bayd[ıi]n\b|ege[-_]",
    re.IGNORECASE,
)

# This guard's own path — must not flag itself.
SELF_PATH = Path(__file__).resolve()

# Skip generated / vendored / VCS / tooling-config trees.
SKIP_DIRS = {
    ".git",
    ".claude",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "coverage",
    "coverage_html",
    "htmlcov",
    "generated",
    ".generated",
    ".next",
}

# Binary / non-text extensions we won't grep into. Filename check still applies.
BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
    ".zip", ".gz", ".tar", ".tgz", ".7z",
    ".docx", ".xlsx", ".pptx",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp4", ".mp3", ".wav",
}


def iter_paths(root: Path):
    for path in root.rglob("*"):
        parts = set(path.relative_to(root).parts)
        if parts & SKIP_DIRS:
            continue
        yield path


def main() -> int:
    # Hit lines may contain non-ASCII (Turkish) characters; make stdout robust
    # on legacy Windows code pages so reporting a hit never crashes the guard.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    name_hits: list[Path] = []
    content_hits: list[tuple[Path, int, str]] = []
    region_hits: list[tuple[Path, int, str]] = []

    for path in iter_paths(REPO_ROOT):
        if path.resolve() == SELF_PATH:
            continue
        rel = path.relative_to(REPO_ROOT)

        if BRAND_RE.search(path.name) or REGION_RE.search(path.name):
            name_hits.append(rel)

        if not path.is_file():
            continue
        if path.suffix.lower() in BINARY_EXTS:
            continue

        try:
            with path.open("r", encoding="utf-8", errors="strict") as fh:
                for lineno, line in enumerate(fh, start=1):
                    if BRAND_RE.search(line):
                        content_hits.append((rel, lineno, line.rstrip("\n")))
                    if REGION_RE.search(line):
                        region_hits.append((rel, lineno, line.rstrip("\n")))
        except (UnicodeDecodeError, OSError):
            continue

    if not name_hits and not content_hits and not region_hits:
        print(f"OK: no '{_FOREIGN_BRAND}' brand or Aegean-region references found.")
        return 0

    if name_hits:
        print("FAIL: file/dir names containing foreign brand/region:")
        for p in name_hits:
            print(f"  {p}")

    if content_hits:
        print("FAIL: file contents containing foreign brand:")
        for p, lineno, line in content_hits:
            print(f"  {p}:{lineno}: {line}")

    if region_hits:
        print("FAIL: file contents containing Aegean-region leakage:")
        for p, lineno, line in region_hits:
            print(f"  {p}:{lineno}: {line}")

    print(
        f"\nTotal: {len(name_hits)} name hit(s), "
        f"{len(content_hits)} brand hit(s), {len(region_hits)} region hit(s)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
