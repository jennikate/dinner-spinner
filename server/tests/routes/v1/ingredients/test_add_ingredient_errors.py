"""
Tests for checking errors when adding an ingredient.

Note: when the ingredient is POST or PATCHed as part of /recipe
Then it is checked on that endpoint/schema
So those tests are under the /recipe folders/unit tests
"""

# =====================================
#  Imports
# =====================================

import pytest

from uuid import UUID

from src.app.schemas.ingredients import IngredientResponseSchema
from src.app.routes.v1.ingredient_routes import add_ingredients
from tests.helpers import serialize_ingredients

# =====================================
#  Body
# =====================================
