from collections.abc import Callable

from sqlalchemy.orm import Session

from db_seeds.seeders.schedule_activity_types import seed as schedule_activity_types
from db_seeds.seeders.student_statuses import seed as student_statuses

SeedFn = Callable[["Session"], object]

# Register new seeders here (import + add to list)
SEEDERS: list[tuple[str, SeedFn]] = [
    ("schedule_activity_type", schedule_activity_types),
    ("student_statuses", student_statuses),
]
