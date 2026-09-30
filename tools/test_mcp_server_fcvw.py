#!/usr/bin/env python3
"""Protocol, tool and boundary tests for the optional read-only MCP server."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mcp_server_fcvw import HANDLERS, TOOLS, handle, serve
from release_layout_fcvw import governed_root


ROOT = governed_root(Path(__file__))


def call(name: str, arguments: dict | None = None, root: Path = ROOT) -> tuple[dict, bool]:
    response = handle(root, {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                             "params": {"name": name, "arguments": arguments or {}}})
    body = response["result"]
    return json.loads(body["content"][0]["text"]), body["isError"]


class ProtocolTests(unittest.TestCase):
    def test_initialize_negotiates_a_supported_version(self) -> None:
        answer = handle(ROOT, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                               "params": {"protocolVersion": "2024-11-05"}})["result"]
        self.assertEqual("2024-11-05", answer["protocolVersion"])
        self.assertIn("tools", answer["capabilities"])
        unknown = handle(ROOT, {"jsonrpc": "2.0", "id": 2, "method": "initialize",
                                "params": {"protocolVersion": "1999-01-01"}})["result"]
        self.assertEqual("2025-06-18", unknown["protocolVersion"])

    def test_notifications_get_no_response_and_errors_are_json_rpc(self) -> None:
        self.assertIsNone(handle(ROOT, {"jsonrpc": "2.0", "method": "notifications/initialized"}))
        self.assertEqual(-32601, handle(ROOT, {"jsonrpc": "2.0", "id": 3, "method": "nope"})["error"]["code"])
        self.assertEqual(-32600, handle(ROOT, {"id": 4, "method": "ping"})["error"]["code"])
        self.assertEqual(-32602, handle(ROOT, {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                                               "params": {"name": "missing"}})["error"]["code"])

    def test_every_listed_tool_has_a_handler_and_a_schema(self) -> None:
        self.assertEqual({tool["name"] for tool in TOOLS}, set(HANDLERS))
        for tool in TOOLS:
            self.assertEqual("object", tool["inputSchema"]["type"])

    def test_stdio_loop_survives_malformed_lines(self) -> None:
        stdin = io.StringIO('not json\n\n{"jsonrpc":"2.0","id":7,"method":"ping"}\n')
        stdout = io.StringIO()
        serve(ROOT, stdin, stdout)
        replies = [json.loads(line) for line in stdout.getvalue().splitlines()]
        self.assertEqual(-32700, replies[0]["error"]["code"])
        self.assertEqual({}, replies[1]["result"])

    def test_cli_process_round_trip(self) -> None:
        script = str(Path(__file__).with_name("mcp_server_fcvw.py"))
        run = subprocess.run([sys.executable, "-B", script, "--root", str(ROOT)],
                             input='{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n',
                             capture_output=True, text=True, timeout=60)
        self.assertEqual(0, run.returncode, run.stderr)
        self.assertEqual(len(TOOLS), len(json.loads(run.stdout)["result"]["tools"]))


class ToolTests(unittest.TestCase):
    def test_routes_match_the_retriever_contract(self) -> None:
        payload, failed = call("fcvw_routes", {"sessions": ["feature"], "events": ["security"]})
        self.assertFalse(failed)
        self.assertIn("FCVW/SECURITY.md", payload["mandatory_paths"])
        self.assertEqual([], payload["mandatory_missing"])
        self.assertIn("FCVW/PLANNING.md", payload["routing"]["ranges"])
        payload, failed = call("fcvw_routes", {"sessions": ["unknown"]})
        self.assertTrue(failed)

    def test_read_sections_returns_outline_or_named_sections(self) -> None:
        outline, failed = call("fcvw_read_sections", {"path": "FCVW/PLANNING.md"})
        self.assertFalse(failed)
        self.assertIn("Regression impact", [item["heading"] for item in outline["outline"]])
        section, _ = call("fcvw_read_sections", {"path": "FCVW/PLANNING.md",
                                                 "headings": ["Regression impact", "Nope"]})
        self.assertIn("## Regression impact", section["content"])
        self.assertNotIn("## Priority queue", section["content"])
        self.assertEqual(["Nope"], section["missing"])

    def test_paths_cannot_escape_the_root(self) -> None:
        for value in ("../outside.md", "/etc/passwd", "FCVW/../../x.md", ""):
            _, failed = call("fcvw_read_sections", {"path": value})
            self.assertTrue(failed, value)
        _, failed = call("fcvw_digest", {"path": "../x.md"})
        self.assertTrue(failed)
        _, failed = call("fcvw_routes", {"active_plan": "../plan.md"})
        self.assertTrue(failed)

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_symlink_out_of_the_root_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            (root / "FCVW").mkdir(parents=True)
            outside = Path(temporary) / "secret.md"
            outside.write_text("# Secret\n", encoding="utf-8")
            (root / "FCVW" / "link.md").symlink_to(outside)
            _, failed = call("fcvw_read_sections", {"path": "FCVW/link.md"}, root.resolve())
            self.assertTrue(failed)

    def test_validate_digest_and_queue(self) -> None:
        report, failed = call("fcvw_validate", {"profile": "clean-template"})
        self.assertFalse(failed)
        self.assertIn("errors", report)
        _, failed = call("fcvw_validate", {"profile": "bogus"})
        self.assertTrue(failed)
        _, failed = call("fcvw_validate", {"since": "--output=/tmp/x"})
        self.assertTrue(failed)
        digest, failed = call("fcvw_digest", {"path": "FCVW/AI.md#token-and-context-budget"})
        self.assertFalse(failed)
        self.assertTrue(digest["source_digest"].startswith("sha256:"))
        _, failed = call("fcvw_digest", {"path": "FCVW/AI.md#no-such-anchor"})
        self.assertTrue(failed)
        queue, failed = call("fcvw_next_plan")
        self.assertFalse(failed)
        self.assertIn("queue", queue)


if __name__ == "__main__":
    unittest.main()
