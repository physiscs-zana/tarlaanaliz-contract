#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


def read_version(text: str) -> str:
    """Extract the contract version string from CONTRACTS_VERSION.md content.

    Canonical format written (and verified) by pin_version.py is
    ``## Version: X.Y.Z``. The previous regex here looked for ``semver: vX.Y.Z``
    which pin_version never emits — so this reader always raised
    ``SystemExit('semver not found')`` and broke sync_to_repos.py (which calls
    it for the sync branch name / PR title). Accept the canonical ``## Version:``
    form (optional ``v`` prefix) and keep the legacy ``semver:`` form as a
    fallback for resilience. Output is normalized to ``vX.Y.Z``.
    """
    m = re.search(r"^##\s*Version:\s*v?(\d+\.\d+\.\d+)\s*$", text, re.MULTILINE)
    if m is None:
        m = re.search(r"^semver:\s*v?(\d+\.\d+\.\d+)\s*$", text, re.MULTILINE)
    if m is None:
        raise SystemExit(
            "version not found in CONTRACTS_VERSION.md "
            "(expected '## Version: X.Y.Z')"
        )
    return f"v{m.group(1)}"


def main() -> int:
    p = Path("CONTRACTS_VERSION.md")
    print(read_version(p.read_text(encoding="utf-8")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
