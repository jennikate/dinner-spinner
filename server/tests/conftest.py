"""
Config for tests.
"""

# =====================================
# Imports
# =====================================

import os
import pytest

from alembic import command
from alembic.config import Config
from sqlalchemy.orm import joinedload, sessionmaker, scoped_session

from src.app import create_app, db as _db # _db to be clear this is the test instance
from src.app.constants import MAX_PER_PAGE
from src.app.models.ingredients import Ingredient 
from src.app.models.recipes import Recipe 
from src.app.models.recipe_ingredients import RecipeIngredient
from src.app.models.units import Unit


# =====================================
# Configuration & setup
# =====================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")

@pytest.fixture
def db():
    """Expose the SQLAlchemy db object for tests."""
    return _db


@pytest.fixture(scope="session")
def app():
    """Create Flask app in testing config and push context."""
    app = create_app("TEST")
    with app.app_context():
        yield app  # app context is active for the duration of the session

@pytest.fixture
def client(app):
    return app.test_client()

# NOTES:
# scope="session": runs once per test session, not per test function.
# autouse=True: automatically applies to all tests — you don’t have to pass it as a parameter.
@pytest.fixture(scope="session", autouse=True)
def apply_migrations(app):
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    
    # Remove the file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Apply migrations with Alembic
    alembic_cfg = Config(os.path.join(MIGRATIONS_DIR, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", MIGRATIONS_DIR)
    alembic_cfg.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])
    command.upgrade(alembic_cfg, "head")
    
    yield
    
    # optional: cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="function", autouse=True)
def session(app):
    """Run each test in its own transaction (rollback after)."""
    connection = _db.engine.connect()
    transaction = connection.begin()

    SessionFactory = sessionmaker(bind=connection, expire_on_commit=False)
    session = scoped_session(SessionFactory)

    _db.session = session

    yield session
    if transaction.is_active:
        transaction.rollback()
    connection.close()
    session.remove()

# =====================================
# Seeds
# =====================================

@pytest.fixture(scope="function")
def seeded_recipes(app, db):
    with app.app_context():
        # ----> Clear all tables to ensure test isolation
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        recipes = [
            Recipe(
                recipe_name="My simple recipe",
                instructions=[
                    {"step_number": 1,"instruction": "First thing you do is"},
                    {"step_number": 2,"instruction": "Second thing you do is"}
                ]
            ),
            Recipe(
                recipe_name="My other recipe",
                instructions=[
                    {"step_number": 1,"instruction": "First thing you do is"},
                    {"step_number": 2,"instruction": "Second thing you do is"}
                ],
                notes="My sample note."
            )
        ]

        db.session.add_all(recipes)
        db.session.commit()

        # Re-query recipes to ensure they are fully loaded and attached
        recipes = db.session.query(Recipe).options(
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.ingredient),
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.unit)
        ).all()

    return recipes


@pytest.fixture(scope="function")
def large_seeded_recipes(app, db):
    """
    Seed many recipes for pagination tests.
    """
    with app.app_context():
        # ----> Clear all tables to ensure test isolation
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        
        recipes = [
            Recipe(
                recipe_name=f"Recipe {i+1}",
                instructions=[{"step_number": 1, "instruction": "Do something"}]
            )
            for i in range(50)  # seed 50 recipes
        ]

        db.session.add_all(recipes)
        db.session.commit()

        # Re-query recipes to ensure they are fully loaded and attached
        # This is needed because the .commit ends the session and detaches objects
        # and they can no longer be reliably accessed in tests
        # joinedload ensures recipe_ingredients and their nested ingredient/unit are eagerly loaded
        # making sure they're available to the tests without lazy loading issues
        recipes = db.session.query(Recipe).options(
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.ingredient),
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.unit)
        ).all()

        return recipes


@pytest.fixture(scope="function")
def seeded_recipes_with_ingredients(app, db):
    """
    Seed recipes with ingredients and units. 
    Each recipe can have a variable number of ingredients.
    """
    with app.app_context():
        # ----> Clear all existing data (important for test isolation)
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        # ---->  Create Ingredients & Units
        ingredient_defs = [
            {"name": "milk"}, 
            {"name": "potato"}, 
            {"name": "pepper"}, 
            {"name": "soy sauce"}
        ]
        ingredients = []
        for i in ingredient_defs:
            ing = Ingredient(ingredient_name=i["name"])
            ingredients.append(ing)

        # TODO: Create Units properly, this is sample hardcoded
        # TODO: Add different amt values as currently everything hardcoded in the code
        units = [Unit(unit_name="pint"), Unit(unit_name="small_item")]
        db.session.add_all(ingredients + units)
        db.session.commit()  # commit to get IDs

        # ----> Define recipes
        recipe_defs = [
            {
                "name": "My simple recipe",
                "instructions": [
                    {"step_number": 1, "instruction": "First thing you do is"},
                    {"step_number": 2, "instruction": "Second thing you do is"}
                ],
                "ingredients": [
                    {"ingredient": ingredients[0], "unit": units[0], "amount": 1},
                    {"ingredient": ingredients[1], "unit": units[1], "amount": 1},
                ],
            },
            {
                "name": "My other recipe",
                "instructions": [
                    {"step_number": 1, "instruction": "First thing you do is"},
                    {"step_number": 2, "instruction": "Second thing you do is"}
                ],
                "notes": "Sample note", # this one has the optional note
                "ingredients": [
                    {"ingredient": ingredients[0], "unit": units[0], "amount": 1},
                    {"ingredient": ingredients[1], "unit": units[1], "amount": 1},
                ]
            },
            {
                "name": "My no ingredient recipe",
                "instructions": [
                    {"step_number": 1, "instruction": "First thing you do is"},
                    {"step_number": 2, "instruction": "Second thing you do is"}
                ],
                "notes": "Sample note", # this one has the optional note
                "ingredients": []  # no ingredients for this one
            }
        ]

        #  ----> Create Recipe and RecipeIngredient objects
        recipes = []
        for rd in recipe_defs: # rd = recipe definition
            r = Recipe(
                recipe_name=rd["name"],
                instructions=rd["instructions"],
                notes=rd.get("notes")
            )
            db.session.add(r)
            db.session.commit()  # commit to get recipe ID

            # Attach ingredients
            for ing_info in rd["ingredients"]: # ing_info = ingredient info
                ri = RecipeIngredient(
                    recipe=r,
                    ingredient=ing_info["ingredient"],
                    unit=ing_info["unit"],
                    amount=ing_info["amount"],
                    ingredient_name=ing_info["ingredient"].ingredient_name,
                    unit_name=ing_info["unit"].unit_name
                )
                db.session.add(ri)
            db.session.commit()

            recipes.append(r)

        #  ----> Re-query fully attached recipes with eager-loading
        recipes = db.session.query(Recipe).options(
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.ingredient),
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.unit)
        ).all()

        return recipes