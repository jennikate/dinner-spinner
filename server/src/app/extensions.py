"""
Extention initialisations.
"""
# =====================================
# Imports
# =====================================

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from sqlalchemy import MetaData

# =====================================
# Body
# =====================================

# Define naming convention for all constraints
# This ensures our migrations are consistent across DB backends
# and helps avoid the `raise ValueError("Constraint must have a name")` when running migrations
naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Pass it into SQLAlchemy metadata
metadata = MetaData(naming_convention=naming_convention)


# Initialize extensions
api = Api()
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
