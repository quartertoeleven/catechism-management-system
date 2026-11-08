"""Enforce Clean Architecture layer boundaries via static import analysis."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# layer -> layers it may import
LAYERS: dict[str, set[str]] = {
    "domain": set(),
    "application": {"domain"},
    "infrastructure": {"domain", "application"},
    "admin_dashboard_api": {"domain", "application", "infrastructure"},
}

SOURCES: dict[str, Path] = {
    "domain": ROOT / "libs/domain/src/domain",
    "application": ROOT / "libs/application/src/application",
    "infrastructure": ROOT / "libs/infrastructure/src/infrastructure",
    "admin_dashboard_api": ROOT / "apps/admin_dashboard_api/src/admin_dashboard_api",
}


def imports_in(tree: ast.AST) -> list[tuple[int, str]]:
    """Return (line number, module name) for absolute imports in a syntax tree."""
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0 or node.module is None:
                continue  # relative import inside same package
            found.append((node.lineno, node.module))
    return found


def check_file(layer: str, path: Path) -> list[str]:
    """Return boundary violations found in a single source file."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    allowed = LAYERS[layer]
    violations: list[str] = []
    for lineno, module in imports_in(tree):
        target = module.split(".", 1)[0]
        if target not in LAYERS or target == layer or target in allowed:
            continue
        violations.append(
            f"{path.relative_to(ROOT)}:{lineno}: "
            f"layer '{layer}' must not import '{target}' "
            f"(allowed: {sorted(allowed) or 'none'})"
        )
    return violations


def main() -> int:
    """Check every layer and return a non-zero exit code on violations."""
    violations: list[str] = []
    for layer, source in SOURCES.items():
        for path in sorted(source.rglob("*.py")):
            violations.extend(check_file(layer, path))

    if violations:
        print("Architecture violations:")
        print("\n".join(violations))
        return 1

    print("Architecture OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
