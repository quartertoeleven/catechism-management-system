import os

import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db_seeds.seeders import SEEDERS


def _run_all() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    engine = create_engine(database_url)
    with Session(engine) as session:
        for name, seed_fn in SEEDERS:
            result = seed_fn(session)
            if isinstance(result, tuple) and len(result) == 2:
                inserted, skipped = result
                print(f"{name}: inserted={inserted} skipped={skipped}")
            else:
                print(f"{name}: done")
        session.commit()
    print(f"Ran {len(SEEDERS)} seeder(s)")


def _list_seeders() -> None:
    if not SEEDERS:
        print("No seeders registered")
        return
    for name, _ in SEEDERS:
        print(name)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="db_seeds", description="Run database seeders"
    )
    parser.add_argument(
        "--list", action="store_true", help="List registered seeders and exit"
    )
    args = parser.parse_args()
    if args.list:
        _list_seeders()
    else:
        _run_all()


if __name__ == "__main__":
    main()
