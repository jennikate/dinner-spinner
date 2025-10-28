"""
Tests for adding an ingredient.
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

class TestAddIngredientStaticMethodWithDbErrors:
    def test_add_new_ingredient_SQLAlchemyError(self, monkeypatch):
        """
        Tests the static method adds ingredients to the db errors correctly
        """
        ingredients_to_add = [{"ingredient_name": "stew"}]
        expected_response = [
            {"ingredient_id": None, "ingredient_name": "stew"}
        ]

        # Monkeypatch db.session.commit to raise SQLAlchemyError
        def bad_commit():
            raise SQLAlchemyError("DB error")
        
        monkeypatch.setattr(_db.session, "commit", bad_commit)

        # Expect the abort() call to raise an HTTPException
        with pytest.raises(HTTPException) as exc_info:
            IngredientService.save_ingredients(ingredients_to_add)

        # Check the abort code and message
        assert exc_info.value.code == 422 or exc_info.value.code == 500
        assert f"Failed to create all ingredients, review and try again. Failed: {expected_response}" in exc_info.value.data["message"]

    
    def test_add_new_ingredient_GenericError(self, monkeypatch):
        """
        Tests the static method adds ingredients to the db errors correctly
        """
        ingredients_to_add = [{"ingredient_name": "Milk"}]
        expected_response = [
            {"ingredient_id": None, "ingredient_name": "milk"}
        ]

        # Monkeypatch db.session.commit to raise GenericError
        def bad_commit():
            raise RuntimeError("Something went wrong!")
        
        monkeypatch.setattr(_db.session, "commit", bad_commit)
        
       # Expect the abort() call to raise an HTTPException
        with pytest.raises(HTTPException) as exc_info:
            IngredientService.save_ingredients(ingredients_to_add)

        # Check the abort code and message
        assert exc_info.value.code == 422 or exc_info.value.code == 500
        assert f"Failed to create all ingredients, review and try again. Failed: {expected_response}" in exc_info.value.data["message"]

