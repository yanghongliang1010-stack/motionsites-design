# MotionSites Design

MotionSites Design is an installable Codex skill for turning a product brief or an existing interface into a distinctive, responsive, and verified frontend implementation.

It ships with eight original offline directions. Optional catalog sync downloads public metadata and an index only; it does not bulk-download prompt bodies or media.

## Install

Requirements: Python 3.10+ and a Codex build with Skills support.

```bash
git clone https://github.com/yanghongliang1010-stack/motionsites-design.git
cd motionsites-design
python3 scripts/install_skill.py
```

Restart Codex, then invoke:

```text
$motionsites-design Redesign this interface while preserving all business logic. Select a direction, implement it in the current stack, and verify desktop and mobile behavior.
```

Update with `git pull` followed by `python3 scripts/install_skill.py --force`.

## Catalog CLI

```bash
python3 scripts/motionsites_catalog.py doctor
python3 scripts/motionsites_catalog.py search "enterprise AI workspace"
python3 scripts/motionsites_catalog.py show ai-operations-cockpit
```

See [docs/INSTALL.md](docs/INSTALL.md), [docs/USAGE.md](docs/USAGE.md), and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## License

Original code, skill instructions, and starter patterns are MIT licensed. Remote catalog material can have separate creator terms and is not bundled. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
