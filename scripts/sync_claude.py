#!/usr/bin/env python3
"""Copy shared Claude Code assets from moto-workspace into each platform repo.

Single-repo cloud sessions only see the repo they clone, so every repo carries
copies of PLATFORM-RULES.md and the agents/skills relevant to it. The source of
truth is this workspace; copies are overwritten and must not be edited in place.

Usage:
    python3 scripts/sync_claude.py            # write copies
    python3 scripts/sync_claude.py --check    # exit 1 if any copy is missing/stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- Synced from moto-workspace/{src} by scripts/sync_claude.py. Do not edit here; edit the source and re-run the sync. -->"
IMPORT_LINE = "@.claude/PLATFORM-RULES.md"
LEDGER = ".claude/.synced"  # list of files this script owns in the repo

COMMON_AGENTS = ["docs-researcher", "vss-schema-guardian", "architecture-guard"]
SAFETY_AGENTS = COMMON_AGENTS + ["safety-reviewer"]
FIRMWARE = {"agents": SAFETY_AGENTS, "skills": ["repo-bootstrap", "feature-module"]}
SOFTWARE = {"agents": COMMON_AGENTS, "skills": ["repo-bootstrap"]}
# Software repos with invariant-8 code: linux-node's OTA, server's OTA packages (ISSUES C-3)
SAFETY_SOFTWARE = {"agents": SAFETY_AGENTS, "skills": ["repo-bootstrap"]}

REPO_ASSETS: dict[str, dict[str, list[str]]] = {
    "moto-vehicle-defs": {"agents": COMMON_AGENTS, "skills": ["signal-change", "repo-bootstrap"]},
    "moto-rt-core": FIRMWARE,
    "moto-safety-node": FIRMWARE,
    "moto-io-node": FIRMWARE,
    "moto-hil-bench": FIRMWARE,
    "moto-connectivity-node": FIRMWARE,  # temporary sole vehicle-bus tester (D-023): tester latch
    "moto-linux-node": SAFETY_SOFTWARE,
    "moto-mcp": SOFTWARE,
    "moto-server": SAFETY_SOFTWARE,
    "moto-ml": SOFTWARE,
    "moto-mobile": SOFTWARE,
}


def with_marker(text: str, src: str) -> str:
    """Insert the marker after YAML frontmatter (or at the top if there is none)."""
    marker = MARKER.format(src=src)
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4) + 5
        return text[:end] + "\n" + marker + "\n" + text[end:]
    return marker + "\n\n" + text


def planned_files(repo: str) -> dict[str, str]:
    """Map repo-relative destination path -> file content."""
    files: dict[str, str] = {}
    rules = (ROOT / "PLATFORM-RULES.md").read_text()
    files[".claude/PLATFORM-RULES.md"] = with_marker(rules, "PLATFORM-RULES.md")
    assets = REPO_ASSETS[repo]
    for name in assets["agents"]:
        src = f".claude/agents/{name}.md"
        files[src] = with_marker((ROOT / src).read_text(), src)
    for name in assets["skills"]:
        src = f".claude/skills/{name}/SKILL.md"
        files[src] = with_marker((ROOT / src).read_text(), src)
    return files


def claude_md_with_import(text: str) -> str:
    if IMPORT_LINE in text:
        return text
    lines = text.splitlines(keepends=True)
    # keep the "# CLAUDE.md — <repo>" title first, import right below it
    return lines[0] + "\n" + IMPORT_LINE + "\n" + "".join(lines[1:])


def sync_repo(repo: str, check: bool) -> list[str]:
    repo_dir = ROOT / repo
    if not repo_dir.is_dir():
        return [f"{repo}: not cloned (run ./setup.sh)"]
    problems: list[str] = []
    files = planned_files(repo)

    ledger_path = repo_dir / LEDGER
    previous = set(ledger_path.read_text().split()) if ledger_path.exists() else set()
    stale = sorted(previous - set(files))

    for rel, content in files.items():
        dest = repo_dir / rel
        if dest.exists() and dest.read_text() == content:
            continue
        problems.append(f"{repo}: {rel} {'stale' if dest.exists() else 'missing'}")
        if not check:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)

    for rel in stale:
        problems.append(f"{repo}: {rel} no longer mapped")
        if not check:
            (repo_dir / rel).unlink(missing_ok=True)

    claude_md = repo_dir / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text()
        if IMPORT_LINE not in text:
            problems.append(f"{repo}: CLAUDE.md lacks {IMPORT_LINE}")
            if not check:
                claude_md.write_text(claude_md_with_import(text))

    ledger = "\n".join(sorted(files)) + "\n"
    if not check and (not ledger_path.exists() or ledger_path.read_text() != ledger):
        ledger_path.write_text(ledger)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report drift, write nothing")
    parser.add_argument("repos", nargs="*", help="limit to these repos (default: all)")
    args = parser.parse_args()

    unknown = set(args.repos) - set(REPO_ASSETS)
    if unknown:
        parser.error(f"unknown repo(s): {', '.join(sorted(unknown))}")

    problems: list[str] = []
    for repo in args.repos or REPO_ASSETS:
        problems += sync_repo(repo, args.check)

    for p in problems:
        print(("DRIFT " if args.check else "synced ") + p)
    if not problems:
        print("all repos in sync")
    return 1 if (args.check and problems) else 0


if __name__ == "__main__":
    sys.exit(main())
