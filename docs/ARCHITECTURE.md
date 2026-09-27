# Architecture

## Components

- `.codex-plugin/plugin.json` describes the full Codex plugin.
- `skills/motionsites-design/SKILL.md` is the decision workflow Codex follows.
- `assets/starter-patterns.json` provides original offline design directions.
- `references/` holds progressive guidance for design, verification, and licensing.
- `scripts/motionsites_catalog.py` searches local content and optionally syncs public metadata.
- `scripts/install_skill.py` creates a self-contained personal Skill installation.

## Data flow

```text
user brief
  -> skill constraints and working mode
  -> offline starter catalog (+ optional synced metadata)
  -> selected direction and visual system
  -> implementation in the user's existing stack
  -> responsive, accessibility, interaction, and runtime verification
```

## Remote sync boundaries

`sync` fetches two small JSON files: catalog metadata and a text-index map. Prompt bodies are not downloaded by sync. The `prompt` command retrieves exactly one indexed text file and requires `--allow-remote`. Media is never fetched.

All remote responses have a size limit. Catalog shape is validated before atomic cache replacement, and indexed prompt paths are checked against traversal.

The helper uses Python's verified HTTPS stack first. If a local Python installation lacks a usable certificate chain, it falls back to system `curl` with TLS verification, timeout, and file-size limits; it never disables certificate validation.

## Extending original patterns

Add an object to `starter-patterns.json` with a unique ID, descriptive metadata, searchable tags, and a complete `direction` object. Keep the pattern original, concrete, and implementable. Add or update tests when search behavior changes.
