"""Compile .po catalogs under a translations directory into .mo files.

Usage:
    uv run scripts/compile_catalogs.py [target]
        target: path to a translations dir containing ``<locale>/LC_MESSAGES/*.po``
                (default: cms_locale's own translations)

Example:
    uv run scripts/compile_catalogs.py ../apps/cms_admin_dashboard_api/translations
"""

from __future__ import annotations

import sys
from pathlib import Path

from babel.messages.frontend import CommandLineInterface

DEFAULT_CATALOGS_DIR = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "cms_locale"
    / "translations"
)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else None
    catalogs_dir = Path(target).resolve() if target else DEFAULT_CATALOGS_DIR

    if not catalogs_dir.is_dir():
        print(f"Catalogs dir not found: {catalogs_dir}")
        return 1

    po_files = sorted(catalogs_dir.glob("*/LC_MESSAGES/*.po"))
    if not po_files:
        print(f"No .po catalogs found under: {catalogs_dir}")
        return 1

    for po_file in po_files:
        locale = po_file.parent.parent.name
        domain = po_file.stem
        print(f"Compiling: {po_file.relative_to(catalogs_dir)}")
        CommandLineInterface().run(
            [
                "pybabel",
                "compile",
                "-i",
                str(po_file),
                "-d",
                str(catalogs_dir),
                "-D",
                domain,
                "-l",
                locale,
            ]
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
