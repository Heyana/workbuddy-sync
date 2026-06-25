#!/usr/bin/env python3
"""PostToolUse hook: auto-detect framework and run analysis after file save.

Supports: Flutter (dart), TypeScript (tsc/vue-tsc), JavaScript (eslint), Go (go vet)

Exit codes:
  0 = analysis passed (or skipped)
  1 = analysis found issues (warning)
  2 = error running analysis
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# --- config ---
DEBOUNCE_SECONDS = 30  # skip if last analysis for this project was < N seconds ago
TIMEOUT_SECONDS = 60   # max time for analysis command
STATE_DIR = Path.home() / ".codebuddy" / ".hook-state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

# --- framework detection ---
def find_project_root(file_path: Path) -> Path | None:
    """Walk up from file to find project root with a marker file."""
    markers = [
        "pubspec.yaml",      # Flutter/Dart
        "go.mod",            # Go
        "package.json",       # Node (JS/TS)
        "tsconfig.json",      # TypeScript
        ".git",               # fallback
    ]
    current = file_path.parent
    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent
    return None

def detect_framework(project_root: Path, file_path: Path) -> tuple[str, list[str]]:
    """Return (framework_name, [command, args...]) or (None, []) if unknown."""
    ext = file_path.suffix.lower()

    # Flutter / Dart
    if ext == ".dart" and (project_root / "pubspec.yaml").exists():
        pubspec = project_root / "pubspec.yaml"
        try:
            content = pubspec.read_text()
            if "flutter" in content.lower():
                return ("flutter", ["flutter", "analyze"])
        except Exception:
            pass
        return ("dart", ["dart", "analyze"])

    # Go
    if ext == ".go" and (project_root / "go.mod").exists():
        return ("go", ["go", "vet", "./..."])

    # Node ecosystem: check if TS project
    if ext in (".ts", ".tsx", ".mts", ".cts"):
        if (project_root / "tsconfig.json").exists():
            # check if Vue project (vue-tsc)
            pkg_json = project_root / "package.json"
            is_vue = False
            if pkg_json.exists():
                try:
                    pkg = json.loads(pkg_json.read_text())
                    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                    is_vue = "vue" in deps or "vue-tsc" in deps
                except Exception:
                    pass
            if is_vue:
                return ("vue-ts", ["npx", "vue-tsc", "--noEmit"])
            return ("tsc", ["npx", "tsc", "--noEmit"])

    # Vue SFC
    if ext == ".vue":
        return ("vue-ts", ["npx", "vue-tsc", "--noEmit"])

    # Plain JS
    if ext in (".js", ".mjs", ".cjs"):
        if (project_root / "package.json").exists():
            return ("eslint", ["npx", "eslint", str(file_path)])

    # CSS / SCSS - stylelint if available
    if ext in (".css", ".scss", ".less"):
        if (project_root / "package.json").exists():
            return ("stylelint", ["npx", "stylelint", str(file_path)])

    return (None, [])

# --- main ---
def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return 0  # no input, nothing to do

    file_path_str = input_data.get("tool_input", {}).get("file_path", "")
    if not file_path_str:
        return 0

    file_path = Path(file_path_str)
    if not file_path.is_absolute():
        file_path = Path(input_data.get("cwd", "")) / file_path
    if not file_path.exists():
        return 0

    project_root = find_project_root(file_path)
    if not project_root:
        return 0

    framework, cmd = detect_framework(project_root, file_path)
    if framework is None:
        return 0  # unsupported file type

    # --- debounce ---
    lock_file = STATE_DIR / f"analyze-{project_root.name}-{framework}.lock"
    now = time.time()
    try:
        if lock_file.exists():
            last_run = float(lock_file.read_text().strip())
            if now - last_run < DEBOUNCE_SECONDS:
                return 0  # skip, ran recently
    except Exception:
        pass
    lock_file.write_text(str(now))

    # --- run analysis ---
    cwd = str(project_root)
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"[auto-analyze] {framework} timed out ({TIMEOUT_SECONDS}s)", file=sys.stderr)
        return 1
    except FileNotFoundError:
        # tool not installed, skip silently
        return 0

    output = (result.stdout + result.stderr).strip()
    if not output:
        return 0

    # truncate long output
    lines = output.split("\n")
    if len(lines) > 50:
        output = "\n".join(lines[:50]) + f"\n... ({len(lines) - 50} more lines)"

    if result.returncode != 0:
        print(f"[auto-analyze] {framework} found issues:", file=sys.stderr)
        print(output, file=sys.stderr)
        return 1  # warning, don't block

    return 0

if __name__ == "__main__":
    sys.exit(min(main(), 2))
