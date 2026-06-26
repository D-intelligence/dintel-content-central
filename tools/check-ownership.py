#!/usr/bin/env python3
"""
Multi-Agent Ownership Verification Script
Project: dintel-content-central (Strapi)
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

# Agent identity from environment
AGENT = os.environ.get("AGENT_AUTHOR", "unknown")

# Valid agents
VALID_AGENTS = {"claude", "gemini", "codex", "human", "ci"}

# Ownership matrix (regex patterns)
OWNERSHIP_MATRIX: Dict[str, List[str]] = {
    "claude": [
        r"^src/api/.*",
        r"^src/admin/.*",
        r"^src/extensions/.*",
        r"^src/bootstrap\.js$",
        r"^src/index\.js$",
        r"^config/.*",
        r"^CLAUDE\.md$",
        r"^MULTI_AGENT_FRAMEWORK\.md$",
    ],
    "gemini": [
        r"^docs/.*",
        r"^README\.md$",
        r"^GEMINI\.md$",
    ],
    "codex": [
        r"^src/components/.*",
        r"^types/.*",
        r"^scripts/.*",
        r"^tests/.*",
        r"^CODEX\.md$",
    ],
}

# Shared files (require Claude approval)
SHARED_FILES = [
    r"^package\.json$",
    r"^yarn\.lock$",
    r"^package-lock\.json$",
    r"^\.github/workflows/.*",
]

# Unrestricted files (anyone can modify)
UNRESTRICTED_FILES = [
    r"^\.agent-state/.*",
    r"^\.gitignore$",
    r"^public/.*",
    r"^\.env.*",
]


def get_file_owner(filepath: str) -> Tuple[Optional[str], str]:
    """Determine file owner and ownership type."""
    # Check unrestricted first
    for pattern in UNRESTRICTED_FILES:
        if re.match(pattern, filepath):
            return None, "unrestricted"

    # Check shared files
    for pattern in SHARED_FILES:
        if re.match(pattern, filepath):
            return "claude", "shared"

    # Check ownership matrix
    for agent, patterns in OWNERSHIP_MATRIX.items():
        for pattern in patterns:
            if re.match(pattern, filepath):
                return agent, "primary"

    return None, "unassigned"


def is_file_locked(filepath: str, root: Path) -> Tuple[bool, Optional[dict]]:
    """Check if file is locked."""
    locks_file = root / ".agent-state" / "locks.yaml"
    if not locks_file.exists():
        return False, None

    with open(locks_file) as f:
        data = yaml.safe_load(f) or {}

    for lock in data.get("locks", []):
        if re.match(lock.get("path", ""), filepath):
            return True, lock

    return False, None


def verify_ownership(files: List[str], agent: str, root: Path) -> Tuple[List[str], List[str]]:
    """Verify agent can modify files."""
    violations = []
    warnings = []

    for filepath in files:
        owner, ownership_type = get_file_owner(filepath)

        if ownership_type == "unrestricted":
            continue

        if ownership_type == "shared":
            if agent != "claude":
                warnings.append(f"{filepath}: Shared file (Claude approval required)")
            continue

        if owner and owner != agent:
            violations.append(f"{filepath}: Owned by {owner}, not {agent}")
            continue

        # Check locks
        is_locked, lock_info = is_file_locked(filepath, root)
        if is_locked and lock_info.get("agent") != agent:
            violations.append(
                f"{filepath}: Locked by {lock_info.get('agent')} "
                f"(task: {lock_info.get('task_id')})"
            )

    return violations, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python check-ownership.py <file1> [file2] ...")
        print("       python check-ownership.py --verify-setup")
        sys.exit(1)

    if sys.argv[1] == "--verify-setup":
        print(f"Agent: {AGENT}")
        print(f"Valid: {AGENT in VALID_AGENTS}")
        root = Path.cwd()
        print(f"State dir: {(root / '.agent-state').exists()}")
        sys.exit(0)

    if AGENT not in VALID_AGENTS:
        print(f"Error: Invalid agent '{AGENT}'")
        print(f"Set AGENT_AUTHOR to one of: {', '.join(VALID_AGENTS)}")
        sys.exit(1)

    root = Path.cwd()
    files = sys.argv[1:]

    violations, warnings = verify_ownership(files, AGENT, root)

    for warning in warnings:
        print(f"WARNING: {warning}")

    for violation in violations:
        print(f"VIOLATION: {violation}")

    if violations:
        sys.exit(1)

    print(f"OK: {len(files)} file(s) verified for agent '{AGENT}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
