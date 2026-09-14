import csv
import os
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from cms_db_models.study_year import ScheduleActivityType

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
    existing_map = {
        row.id: row
        for row in session.scalars(select(ScheduleActivityType)).all()
    }

    inserted = 0
    updated = 0
    for r in rows:
        row_id = int(r["id"])
        if row_id in existing_map:
            existing = existing_map[row_id]
            existing.color = r["color"]
            existing.is_system = _parse_bool(r["is_system"])
            updated += 1
        else:
            session.add(
                ScheduleActivityType(
                    id=row_id,
                    code=r["code"],
                    name=r["name"],
                    color=r["color"],
                    is_system=_parse_bool(r["is_system"]),
                )
            )
            inserted += 1
    __print_result(inserted, updated)
    return inserted, updated


def __print_result(inserted: int, updated: int) -> None:
    print(f"ScheduleActivityType seed: inserted={inserted} updated={updated}")


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    engine = create_engine(database_url)
    with Session(engine) as session:
        seed(session)
        session.commit()


if __name__ == "__main__":
    main()
