"""Generate the OpenAPI specification for the Admin Dashboard API."""

import json
from pathlib import Path
from typing import Final

from admin_dashboard_api.main import create_app

OPENAPI_FILE: Final[Path] = Path("openapi.json")
TAG_SEPARATOR: Final[str] = "-"


def generate_spec() -> None:
    """Write the FastAPI-generated OpenAPI schema to ``openapi.json``."""
    openapi_schema = create_app().openapi()
    with OPENAPI_FILE.open("w") as file:
        json.dump(openapi_schema, file, indent=2)


def beautify_operation_ids() -> None:
    """Strip the leading tag name from every operation ID."""
    openapi_content = json.loads(OPENAPI_FILE.read_text())

    for path_data in openapi_content["paths"].values():
        for operation in path_data.values():
            tags = operation.get("tags", [])
            operation_id = operation.get("operationId", "")
            if not tags:
                continue

            tag_prefix = f"{tags[0]}{TAG_SEPARATOR}"
            if operation_id.startswith(tag_prefix):
                operation["operationId"] = operation_id[len(tag_prefix) :]

    OPENAPI_FILE.write_text(json.dumps(openapi_content))


if __name__ == "__main__":
    generate_spec()
    beautify_operation_ids()
