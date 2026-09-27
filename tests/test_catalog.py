from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "motionsites_catalog.py"
SPEC = importlib.util.spec_from_file_location("motionsites_catalog", SCRIPT)
assert SPEC and SPEC.loader
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def test_starter_search_finds_enterprise_ai_direction(self) -> None:
        matches = catalog.search_entries(catalog.starter_entries(), "enterprise AI 后台", None, 3)
        self.assertTrue(matches)
        self.assertEqual(matches[0]["id"], "ai-operations-cockpit")

    def test_category_filter(self) -> None:
        matches = catalog.search_entries(catalog.starter_entries(), "", "commerce", 10)
        self.assertEqual([item["id"] for item in matches], ["tactile-commerce"])

    def test_safe_prompt_path_rejects_traversal(self) -> None:
        with self.assertRaises(catalog.CatalogError):
            catalog.safe_prompt_path("catalog-text/../../secret.txt")

    def test_sync_works_with_local_file_urls_without_prompt_download(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            remote = temp / "remote"
            cache = temp / "cache"
            remote.mkdir()
            meta = [{"id": "remote-one", "title": "Remote One", "category": "demo"}]
            index = {"remote-one": "catalog-text/remote-one.txt"}
            (remote / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
            (remote / "index.json").write_text(json.dumps(index), encoding="utf-8")

            args = type("Args", (), {
                "catalog_url": (remote / "meta.json").as_uri(),
                "index_url": (remote / "index.json").as_uri(),
                "cache_dir": cache,
                "json": False,
            })()
            self.assertEqual(catalog.command_sync(args), 0)
            self.assertEqual(catalog.synced_entries(cache)[0]["id"], "remote-one")
            self.assertFalse((cache / "catalog-text" / "remote-one.txt").exists())

    def test_prompt_requires_explicit_remote_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            args = type("Args", (), {
                "id": "remote-one",
                "allow_remote": False,
                "cache_dir": Path(temp_name),
                "data_base": "https://example.invalid/",
            })()
            with self.assertRaises(catalog.CatalogError):
                catalog.command_prompt(args)


if __name__ == "__main__":
    unittest.main()
