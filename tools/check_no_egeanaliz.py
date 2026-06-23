#!/usr/bin/env python3
"""
Rebrand guard: ensures the old brand "EgeAnaliz" never reappears in the repo.

Checks (case-insensitive):
  1. File and directory names containing the contiguous brand "egeanaliz".
  2. File contents containing the contiguous brand "egeanaliz".

The current brand "tarlaanaliz" never produces the "egeanaliz" substring, so
it is not flagged. Generated coverage reports are skipped, and files in
ALLOWLIST (which legitimately reference the sibling egeanaliz distribution,
e.g. CHANGELOG.md) are exempt.

Exits 1 on any hit, 0 if clean.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Contiguous legacy brand only. The regex is assembled from parts so this
# guard's own source does not contain the literal brand and self-match.
# Only the contiguous "egeanaliz" form is matched; the current brand
# "tarlaanaliz" and unrelated phrases never produce this substring.
_LEGACY_BRAND = "ege" + "analiz"
BRAND_RE = re.compile(_LEGACY_BRAND, re.IGNORECASE)

# This guard's own path — must not flag itself.
SELF_PATH = Path(__file__).resolve()

# Skip generated / vendored / VCS / tooling-config trees.
SKIP_DIRS = {
    ".git",
    ".claude",  # Claude Code local config; out of contract scope
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
    "coverage_html",  # generated HTML coverage report (gitignored)
    "htmlcov",        # default coverage HTML dir name (gitignored)
    ".next",
}

# Generated report files (gitignored) that may exist locally after a test run.
SKIP_FILES = {
    ".coverage",
    "coverage.xml",
}

# Files permitted to mention the legacy brand for legitimate cross-referencing
# — e.g. documenting that egeanaliz is a SEPARATE sibling distribution. These
# are intentional historical references, not rebrand leftovers.
ALLOWLIST = {
    Path("CHANGELOG.md"),
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
    name_hits: list[Path] = []
    content_hits: list[tuple[Path, int, str]] = []

    for path in iter_paths(REPO_ROOT):
        if path.resolve() == SELF_PATH:
            continue
        rel = path.relative_to(REPO_ROOT)

        if rel in ALLOWLIST or path.name in SKIP_FILES:
            continue

        if BRAND_RE.search(path.name):
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
        except (UnicodeDecodeError, OSError):
            # Treat undecodable files as binary; filename check above still ran.
            continue

    if not name_hits and not content_hits:
        print(f"OK: no '{_LEGACY_BRAND}' brand references found.")
        return 0

    if name_hits:
        print("FAIL: file/dir names containing old brand:")
        for p in name_hits:
            print(f"  {p}")

    if content_hits:
        print("FAIL: file contents containing old brand:")
        for p, lineno, line in content_hits:
            print(f"  {p}:{lineno}: {line}")

    print(
        f"\nTotal: {len(name_hits)} name hit(s), {len(content_hits)} content hit(s)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
