"""
Tests for randomly returning recipes.
"""

# =====================================
#  Imports
# =====================================

import pytest

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from src.app.extensions import db as _db
from src.app.services.ingredient_services import IngredientService

from tests.helpers import serialize_ingredients


# =====================================
#  Body
# =====================================


# invalid default amount (string, 0) -> returns default amt
# invalid uuid
# valid uuid but recipe not found

