"""
Tests for the repr definitions in models.
"""

# =====================================
#  Imports
# =====================================

from src.app.models import Ingredient, IngredientType, RecipeIngredient, Unit

# =====================================
#  Body
# =====================================

def test_ingredient_repr_exact():
    ri = Ingredient(ingredient_name="Milk")
    assert repr(ri) == "<Ingredient: Milk>"


def test_ingredienttype_repr_exact():
    ri = IngredientType(ingredient_type="Fresh")
    assert repr(ri) == "<ingredient_type: Fresh>"


def test_recipeingredient_repr_exact():
    ri = RecipeIngredient(
        amount=42,
        unit=Unit(unit_name="ml"),
        ingredient=Ingredient(ingredient_name="Milk")
    )
    assert repr(ri) == "<RecipeIngredient: 42 ml of Milk>"


def test_unit_repr_exact():
    ri = Unit(
        unit_name="tablespoon",
        abbreviation="tbsp"
    )
    assert repr(ri) == "<unit: tablespoon, abbreviation tbsp>"

