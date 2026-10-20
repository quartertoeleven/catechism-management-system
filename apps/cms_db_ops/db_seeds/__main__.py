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
    failed: list[str] = []
    with Session(engine) as session:
        for name, seed_fn in SEEDERS:
            try:
                seed_fn(session)
            except Exception:
                failed.append(name)
        session.commit()

    total = len(SEEDERS)
    succeeded = total - len(failed)
    print(f"Ran {total} seeder(s): {succeeded} succeeded, {len(failed)} failed")
    if failed:
        print(f"Failed: {', '.join(failed)}")


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
