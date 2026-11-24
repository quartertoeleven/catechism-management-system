"""Central SQLAlchemy metadata registry for Alembic autogenerate."""

from sqlalchemy import MetaData

from infrastructure.persistence.base import Base
from infrastructure.persistence.directory import catechist
from infrastructure.persistence.master_data import catechist_title

# Importing a model module registers its tables on Base.metadata.
_MODEL_MODULES = (catechist, catechist_title)

TARGET_METADATA: MetaData = Base.metadata
