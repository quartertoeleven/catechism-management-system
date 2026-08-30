import csv
import os
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from cms_db_models.directory import StudentStatus

CSV_PATH = (
    Path(__file__).resolve().parent.parent / "seed_data" / f"{Path(__file__).stem}.csv"
)


def _read_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "t")


def seed(session: Session) -> tuple[int, int]:
    rows = _read_rows(CSV_PATH)
    existing_ids = set(session.scalars(select(StudentStatus.id)).all())
    new_rows = [r for r in rows if int(r["id"]) not in existing_ids]

    inserted = 0
    skipped = len(rows) - len(new_rows)
    if new_rows:
        session.add_all(
            StudentStatus(
                id=int(r["id"]),
                code=r["code"],
                name=r["name"],
                is_default=_parse_bool(r["is_default"]),
            )
            for r in new_rows
        )
        inserted = len(new_rows)
    return inserted, skipped


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    engine = create_engine(database_url)
    with Session(engine) as session:
        inserted, skipped = seed(session)
        session.commit()
    print(f"StudentStatus seed: inserted={inserted} skipped={skipped}")


if __name__ == "__main__":
    main()
