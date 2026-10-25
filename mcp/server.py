#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publish-to-all-skill-stores — MCP server (stdio, zero dependencies).

Exposes the skill's three tools over the Model Context Protocol so that any
MCP-capable agent (Claude Code, Cursor, Codex, OpenClaw, …) can call them
without knowing this repo's layout.

    python mcp/server.py            # speaks JSON-RPC 2.0 on stdin/stdout

Tools
  skill_store_registry  list the 36 publishing channels (region / form / pricing)
  skill_preflight       readiness check for a skill folder
  skill_build_package   build the zip shape stores ask for

Everything runs locally. No network except the public endpoints the scripts
themselves target when you ask them to submit.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL = os.path.join(ROOT, "skills", "publish-to-all-skill-stores")
SCRIPTS = os.path.join(SKILL, "scripts")

PROTOCOL_VERSION = "2025-06-18"

TOOLS = [
    {
        "name": "skill_store_registry",
        "description": (
            "List every agent-skill store this project knows about, with region "
            "(global/cn), submission form (api/pr/cli/form/auto/tool/port) and "
            "whether the channel supports paid listings."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "skill_preflight",
        "description": (
            "Check whether a skill folder is ready to be published: repo layout "
            "(skills/<name>/SKILL.md), LICENSE, danger calls, network behaviour, "
            "and whether the path matches the paths directory crawlers scan."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_dir": {"type": "string", "description": "Absolute path to the skill folder."},
            },
            "required": ["skill_dir"],
            "additionalProperties": False,
        },
    },
    {
        "name": "skill_build_package",
        "description": (
            "Build the packages stores expect. Produces a skillroot zip "
            "(SKILL.md at the root of a single top-level folder) plus a manifest."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "Repository root, absolute path."},
                "skill_subdir": {"type": "string", "description": "Path of the skill inside the repo, e.g. skills/my-skill."},
                "out_dir": {"type": "string", "description": "Output directory. Default: <repo>/dist"},
            },
            "required": ["repo", "skill_subdir"],
            "additionalProperties": False,
        },
    },
]


def _run(script: str, args: list[str]) -> dict[str, Any]:
    cmd = [sys.executable, os.path.join(SCRIPTS, script), *args]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=300)
    out = (proc.stdout or "") + (proc.stderr or "")
    return {"exit_code": proc.returncode, "output": out[-8000:]}


def call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "skill_store_registry":
        res = _run("submit_all.py", ["--registry"])
        return {"content": [{"type": "text", "text": res["output"]}]}

    if name == "skill_preflight":
        path = args.get("skill_dir", "")
        if not os.path.isdir(path):
            return {"content": [{"type": "text", "text": f"not a directory: {path}"}], "isError": True}
        res = _run("preflight.py", [path])
        return {"content": [{"type": "text", "text": res["output"]}],
                "isError": res["exit_code"] not in (0, 1)}

    if name == "skill_build_package":
        repo = args.get("repo", "")
        sub = args.get("skill_subdir", "")
        out = args.get("out_dir") or os.path.join(repo, "dist")
        if not os.path.isdir(os.path.join(repo, sub)):
            return {"content": [{"type": "text", "text": f"skill not found: {os.path.join(repo, sub)}"}], "isError": True}
        res = _run("build_package.py", [repo, sub, "--out", out])
        return {"content": [{"type": "text", "text": res["output"]}],
                "isError": res["exit_code"] != 0}

    return {"content": [{"type": "text", "text": f"unknown tool: {name}"}], "isError": True}


def handle(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "publish-to-all-skill-stores", "version": "2.0.0"},
        }}

    if method in ("notifications/initialized", "initialized"):
        return None

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments") or {}
        try:
            return {"jsonrpc": "2.0", "id": mid, "result": call_tool(name, args)}
        except Exception as exc:  # noqa: BLE001
            return {"jsonrpc": "2.0", "id": mid,
                    "result": {"content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
                               "isError": True}}

    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}

    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"method not found: {method}"}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
