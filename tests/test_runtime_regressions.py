from __future__ import annotations

import ast
import unittest
from pathlib import Path

from src.video_app.core import service, storage


class ProviderStatusNormalizationTests(unittest.TestCase):
    def test_normalizes_known_openai_statuses(self) -> None:
        self.assertEqual(
            service._normalize_provider_status("processing", provider="openai", video_id="video-1"),
            "in_progress",
        )
        self.assertEqual(
            service._normalize_provider_status("succeeded", provider="openai", video_id="video-1"),
            "completed",
        )
        self.assertEqual(
            service._normalize_provider_status("cancelled", provider="openai", video_id="video-1"),
            "failed",
        )

    def test_unknown_status_defaults_to_in_progress_without_leaking_provider_value(self) -> None:
        self.assertEqual(
            service._normalize_provider_status("provider_specific_state", provider="openai", video_id="video-2"),
            "in_progress",
        )


class CoreBoundaryTests(unittest.TestCase):
    def test_core_storage_no_longer_exposes_cli_last_video_id_helpers(self) -> None:
        self.assertFalse(hasattr(storage, "save_last_video_id"))
        self.assertFalse(hasattr(storage, "load_last_video_id"))


class AppImportSafetyTests(unittest.TestCase):
    def test_app_module_exports_module_level_app(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        module = ast.parse(app_path.read_text(encoding="utf-8"))

        module_level_app_assignments = [
            node
            for node in module.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "app" for target in node.targets)
        ]

        self.assertEqual(len(module_level_app_assignments), 1)

    def test_app_module_exposes_explicit_create_app_function(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        module = ast.parse(app_path.read_text(encoding="utf-8"))

        create_app_functions = [
            node
            for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name == "create_app"
        ]

        self.assertEqual(len(create_app_functions), 1)

    def test_app_module_does_not_run_server_at_import_time(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        module = ast.parse(app_path.read_text(encoding="utf-8"))

        module_level_run_calls = [
            node
            for node in module.body
            if isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == "run"
        ]

        self.assertEqual(module_level_run_calls, [])


class BrowserRestoreSafetyTests(unittest.TestCase):
    def test_new_generation_clears_persisted_task_before_fetch(self) -> None:
        app_js_path = Path(__file__).resolve().parents[1] / "static" / "app.js"
        source = app_js_path.read_text(encoding="utf-8")

        clear_call = source.index("clearPersistedTaskId();")
        fetch_call = source.index('const response = await fetch("/generate", {')

        self.assertLess(clear_call, fetch_call)


if __name__ == "__main__":
    unittest.main()
