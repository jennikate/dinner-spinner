"""
Tests for adding an ingredient.
"""

# =====================================
#  Imports
# =====================================

import pytest

from sqlalchemy.exc import SQLAlchemyError

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
        ingredients = [{"ingredient_name": "stew"}]

        # Monkeypatch db.session.commit to raise SQLAlchemyError
        def bad_commit():
            raise SQLAlchemyError("DB error")
        
        monkeypatch.setattr(_db.session, "commit", bad_commit)
        response = IngredientService.save_ingredients(ingredients)

        # We don't call abort on this method as we want to respond to user
        # with what failed to save so they can decide next step
        # we save anything that works
        expected_response = {
            "failed": [
                {
                    "ingredient_name": "stew"
                }
            ], 
            "saved": []    
        }

        assert {
            "saved": serialize_ingredients(response["saved"]),
            "failed": serialize_ingredients(response["failed"])
        } == expected_response

    
    def test_add_new_ingredient_GenericError(self, monkeypatch):
        """
        Tests the static method adds ingredients to the db errors correctly
        """
        ingredients = [{"ingredient_name": "Milk"}]

        # Monkeypatch db.session.commit to raise GenericError
        def bad_commit():
            raise RuntimeError("Something went wrong!")
        
        monkeypatch.setattr(_db.session, "commit", bad_commit)
        response = IngredientService.save_ingredients(ingredients)

        expected_response = {
            "failed": [
                {
                    "ingredient_name": "milk" # gets converted to lowercase
                }
            ], 
            "saved": []    
        }

        assert {
            "saved": serialize_ingredients(response["saved"]),
            "failed": serialize_ingredients(response["failed"])
        } == expected_response

