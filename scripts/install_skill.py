#!/usr/bin/env python3
"""Install the bundled skill into a user's Codex skill directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "motionsites-design"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path("~/.codex/skills/motionsites-design").expanduser())
    parser.add_argument("--force", action="store_true", help="Replace an existing installation")
    args = parser.parse_args()
    target = args.destination.expanduser().resolve()
    if target.exists():
        if not args.force:
            parser.error(f"destination exists: {target}; pass --force to replace it")
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, target)
    bundled_scripts = target / "scripts"
    bundled_scripts.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "scripts" / "motionsites_catalog.py", bundled_scripts / "motionsites_catalog.py")
    print(f"Installed motionsites-design skill at {target}")
    print("Restart Codex, then invoke it with: $motionsites-design")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
