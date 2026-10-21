"""grade leader and vice leader catechists optional

Revision ID: 9e4f1c8a27b3
Revises: 35a6c4023799
Create Date: 2026-10-21 17:45:47.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e4f1c8a27b3"
down_revision: Union[str, Sequence[str], None] = "35a6c4023799"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "grades",
        "leader_catechist_id",
        existing_type=sa.Uuid(),
        nullable=True,
        schema="study_year",
    )
    op.alter_column(
        "grades",
        "vice_leader_catechist_id",
        existing_type=sa.Uuid(),
        nullable=True,
        schema="study_year",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Fails if any grade row has NULL leader/vice leader.
    op.alter_column(
        "grades",
        "leader_catechist_id",
        existing_type=sa.Uuid(),
        nullable=False,
        schema="study_year",
    )
    op.alter_column(
        "grades",
        "vice_leader_catechist_id",
        existing_type=sa.Uuid(),
        nullable=False,
        schema="study_year",
    )
