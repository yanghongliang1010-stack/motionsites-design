# Installation

## Skill-only installation (recommended)

```bash
git clone https://github.com/yanghongliang1010-stack/motionsites-design.git
cd motionsites-design
python3 scripts/install_skill.py
```

The installer copies the Skill, its original patterns, references, UI metadata, and the catalog helper to `~/.codex/skills/motionsites-design`. It refuses to overwrite an existing installation unless `--force` is supplied.

Restart Codex after installing or updating.

### Custom destination

```bash
python3 scripts/install_skill.py --destination /absolute/path/to/skills/motionsites-design
```

### Update

```bash
git pull
python3 scripts/install_skill.py --force
```

### Uninstall

Remove only the installed `motionsites-design` directory from your personal Codex skills folder. The cloned source repository and optional catalog cache are separate.

## Full plugin development installation

Maintainers can validate `.codex-plugin/plugin.json`, place the repository under their personal plugin source directory, register it in their personal marketplace, and install `motionsites-design@personal` with Codex's plugin tooling. The Skill-only path is intentionally simpler for end users.

## Verify

```bash
python3 scripts/motionsites_catalog.py doctor --json
python3 scripts/motionsites_catalog.py search "dashboard" --source starter --json
python3 -m unittest discover -s tests -v
```

Expected results: eight starter entries, a writable or not-yet-created cache path, matching search output, and passing tests. Network access is not needed.

## Optional remote metadata

```bash
python3 scripts/motionsites_catalog.py sync
```

This writes metadata and a text index to `~/.cache/motionsites-design`. It does not download media or prompt bodies. Override the cache with `MOTIONSITES_DESIGN_CACHE` or `--cache-dir`.

## Troubleshooting

- **Skill is not listed:** confirm `~/.codex/skills/motionsites-design/SKILL.md` exists, then restart Codex.
- **Existing destination:** rerun with `--force` only after confirming the target is this Skill.
- **Sync fails:** continue offline; starter patterns are sufficient.
- **No remote prompt:** run `sync` first, confirm the ID, and use `--allow-remote` only after reviewing licensing terms.
