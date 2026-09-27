#!/usr/bin/env python3
"""Search an offline design catalog and optionally sync public metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_STARTERS = ROOT / "skills" / "motionsites-design" / "assets" / "starter-patterns.json"
SKILL_STARTERS = ROOT / "assets" / "starter-patterns.json"
STARTERS = PLUGIN_STARTERS if PLUGIN_STARTERS.exists() else SKILL_STARTERS
DEFAULT_CACHE = Path(os.environ.get("MOTIONSITES_DESIGN_CACHE", "~/.cache/motionsites-design")).expanduser()
DEFAULT_META_URL = "https://raw.githubusercontent.com/zhaosenlin12-creator/MotionSites/main/data/catalog-meta.json"
DEFAULT_INDEX_URL = "https://raw.githubusercontent.com/zhaosenlin12-creator/MotionSites/main/data/catalog-text-index.json"
DEFAULT_DATA_BASE = "https://raw.githubusercontent.com/zhaosenlin12-creator/MotionSites/main/data/"
MAX_DOWNLOAD = 10 * 1024 * 1024


class CatalogError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError(f"Cannot read valid JSON from {path}: {exc}") from exc


def validate_entries(value: Any, source: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise CatalogError(f"{source} must contain a JSON array")
    valid: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not isinstance(item.get("title"), str):
            continue
        copy = dict(item)
        copy.setdefault("description", "")
        copy.setdefault("category", "uncategorized")
        copy.setdefault("type", "unknown")
        copy.setdefault("tags", [])
        copy.setdefault("source_kind", "remote")
        valid.append(copy)
    return valid


def starter_entries() -> list[dict[str, Any]]:
    return validate_entries(read_json(STARTERS), str(STARTERS))


def cache_paths(cache_dir: Path) -> tuple[Path, Path]:
    return cache_dir / "catalog-meta.json", cache_dir / "catalog-text-index.json"


def synced_entries(cache_dir: Path) -> list[dict[str, Any]]:
    meta_path, _ = cache_paths(cache_dir)
    if not meta_path.exists():
        return []
    entries = validate_entries(read_json(meta_path), str(meta_path))
    for entry in entries:
        entry["source_kind"] = "remote"
    return entries


def all_entries(cache_dir: Path, source: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if source in {"all", "starter"}:
        entries.extend(starter_entries())
    if source in {"all", "synced"}:
        entries.extend(synced_entries(cache_dir))
    return entries


def normalized_terms(query: str) -> list[str]:
    return [term for term in re.split(r"[^\w\u3400-\u9fff]+", query.casefold()) if term]


def searchable_text(entry: dict[str, Any]) -> str:
    fields = [entry.get("id", ""), entry.get("title", ""), entry.get("description", ""), entry.get("category", ""), entry.get("type", "")]
    tags = entry.get("tags", [])
    if isinstance(tags, list):
        fields.extend(str(tag) for tag in tags)
    return " ".join(str(field) for field in fields).casefold()


def score_entry(entry: dict[str, Any], query: str) -> int:
    query_normalized = query.casefold().strip()
    if not query_normalized:
        return 1
    haystack = searchable_text(entry)
    title = str(entry.get("title", "")).casefold()
    score = 0
    if query_normalized in title:
        score += 20
    if query_normalized in haystack:
        score += 10
    for term in normalized_terms(query):
        if term.isascii() and term.replace("_", "").isalnum():
            title_match = re.search(rf"(?<![a-z0-9_]){re.escape(term)}(?![a-z0-9_])", title) is not None
            text_match = re.search(rf"(?<![a-z0-9_]){re.escape(term)}(?![a-z0-9_])", haystack) is not None
        else:
            title_match = term in title
            text_match = term in haystack
        if title_match:
            score += 6
        elif text_match:
            score += 2
    return score


def project_entry(entry: dict[str, Any]) -> dict[str, Any]:
    keys = ("id", "title", "description", "category", "type", "source_kind", "tags", "is_free", "direction")
    return {key: entry[key] for key in keys if key in entry}


def search_entries(entries: list[dict[str, Any]], query: str, category: str | None, limit: int) -> list[dict[str, Any]]:
    ranked: list[tuple[int, dict[str, Any]]] = []
    for entry in entries:
        if category and str(entry.get("category", "")).casefold() != category.casefold():
            continue
        score = score_entry(entry, query)
        if score > 0:
            ranked.append((score, entry))
    ranked.sort(key=lambda pair: (-pair[0], str(pair[1].get("title", "")).casefold()))
    return [project_entry(entry) | {"score": score} for score, entry in ranked[:limit]]


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "motionsites-design/0.1 (+open-source catalog helper)"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            size_header = response.headers.get("Content-Length")
            if size_header and int(size_header) > MAX_DOWNLOAD:
                raise CatalogError(f"Remote file exceeds {MAX_DOWNLOAD} bytes")
            payload = response.read(MAX_DOWNLOAD + 1)
    except (OSError, urllib.error.URLError, ValueError) as exc:
        curl = shutil.which("curl")
        if not curl:
            raise CatalogError(f"Download failed for {url}: {exc}") from exc
        fallback = subprocess.run(
            [curl, "-fsSL", "--max-time", "20", "--max-filesize", str(MAX_DOWNLOAD), url],
            check=False,
            capture_output=True,
        )
        if fallback.returncode != 0:
            message = fallback.stderr.decode("utf-8", errors="replace").strip()
            raise CatalogError(f"Download failed for {url}: {message or exc}") from exc
        payload = fallback.stdout
    if len(payload) > MAX_DOWNLOAD:
        raise CatalogError(f"Remote file exceeds {MAX_DOWNLOAD} bytes")
    return payload


def download_json(url: str) -> Any:
    try:
        return json.loads(download(url).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CatalogError(f"Remote response is not valid UTF-8 JSON: {url}") from exc


def atomic_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def command_search(args: argparse.Namespace) -> int:
    entries = all_entries(args.cache_dir, args.source)
    matches = search_entries(entries, args.query, args.category, args.limit)
    if args.json:
        print_json(matches)
    elif not matches:
        print("No matching design directions found.")
    else:
        for entry in matches:
            print(f"{entry['id']}  [{entry.get('category', 'uncategorized')}]  {entry['title']}")
            print(f"  {entry.get('description', '')}")
            print(f"  source={entry.get('source_kind', 'unknown')} score={entry['score']}")
    return 0


def command_show(args: argparse.Namespace) -> int:
    match = next((item for item in all_entries(args.cache_dir, "all") if item.get("id") == args.id), None)
    if match is None:
        raise CatalogError(f"Unknown design id: {args.id}")
    if args.json:
        print_json(project_entry(match))
    else:
        print_json(project_entry(match))
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    meta_path, index_path = cache_paths(args.cache_dir)
    status = {
        "plugin_root": str(ROOT),
        "starter_catalog": str(STARTERS),
        "starter_count": len(starter_entries()),
        "cache_dir": str(args.cache_dir),
        "synced_count": len(synced_entries(args.cache_dir)),
        "metadata_cached": meta_path.exists(),
        "text_index_cached": index_path.exists(),
    }
    if args.json:
        print_json(status)
    else:
        for key, value in status.items():
            print(f"{key}: {value}")
    return 0


def command_sync(args: argparse.Namespace) -> int:
    metadata = download_json(args.catalog_url)
    index = download_json(args.index_url)
    validated = validate_entries(metadata, args.catalog_url)
    if not isinstance(index, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in index.items()):
        raise CatalogError("The remote text index must be a string-to-string JSON object")
    meta_path, index_path = cache_paths(args.cache_dir)
    atomic_json_write(meta_path, validated)
    atomic_json_write(index_path, index)
    result = {"synced": len(validated), "cache_dir": str(args.cache_dir), "prompts_downloaded": 0}
    print_json(result) if args.json else print(f"Synced {len(validated)} metadata entries to {args.cache_dir}; prompt bodies downloaded: 0")
    return 0


def safe_prompt_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not value.startswith("catalog-text/") or path.suffix != ".txt":
        raise CatalogError("Unsafe prompt path in remote index")
    return value


def command_prompt(args: argparse.Namespace) -> int:
    if not args.allow_remote:
        raise CatalogError("Remote prompt download requires --allow-remote. Review third-party terms before use.")
    _, index_path = cache_paths(args.cache_dir)
    if not index_path.exists():
        raise CatalogError("No synced text index. Run sync first with network access.")
    index = read_json(index_path)
    if not isinstance(index, dict) or args.id not in index:
        raise CatalogError(f"No prompt path indexed for: {args.id}")
    relative = safe_prompt_path(str(index[args.id]))
    url = urllib.parse.urljoin(args.data_base.rstrip("/") + "/", relative)
    body = download(url).decode("utf-8")
    prompt_path = args.cache_dir / relative
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = prompt_path.with_suffix(".txt.tmp")
    temporary.write_text(body, encoding="utf-8")
    temporary.replace(prompt_path)
    print(body, end="" if body.endswith("\n") else "\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(cache_dir=DEFAULT_CACHE)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search starter and optionally synced metadata")
    search.add_argument("query")
    search.add_argument("--category")
    search.add_argument("--source", choices=("all", "starter", "synced"), default="all")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    search.add_argument("--json", action="store_true")
    search.set_defaults(handler=command_search)

    show = subparsers.add_parser("show", help="Show one design direction")
    show.add_argument("id")
    show.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    show.add_argument("--json", action="store_true")
    show.set_defaults(handler=command_show)

    doctor = subparsers.add_parser("doctor", help="Inspect local catalog status")
    doctor.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(handler=command_doctor)

    sync = subparsers.add_parser("sync", help="Download public metadata and text index only")
    sync.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    sync.add_argument("--catalog-url", default=DEFAULT_META_URL)
    sync.add_argument("--index-url", default=DEFAULT_INDEX_URL)
    sync.add_argument("--json", action="store_true")
    sync.set_defaults(handler=command_sync)

    prompt = subparsers.add_parser("prompt", help="Fetch one indexed prompt after explicit consent")
    prompt.add_argument("id")
    prompt.add_argument("--allow-remote", action="store_true")
    prompt.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    prompt.add_argument("--data-base", default=DEFAULT_DATA_BASE)
    prompt.set_defaults(handler=command_prompt)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "limit") and args.limit < 1:
        parser.error("--limit must be at least 1")
    try:
        return int(args.handler(args))
    except CatalogError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
