# Dinner Spinner - Server

Requirements
- Python 3.13
- SQLite

---

## Docs

- [Installation](../docs/server/installation.md)
- [Development](../docs/server/development.md)

## Important Notes

**Ingredient Type**

While the model exists, this has not been implemented into functionality.
It will be added in a later version.


**When writing documentation for use**
When adding ingredients as part of POST or PATCH a recipe, the ingredients are handled as separate entities.

Therefore you can successfully add a recipe and some of it's ingredients, while other ingredients fail to save.

TODO
If an ingredient fails to save the POST/PATCH will return a 201 but include info on the failed to create ingredients so client can take appropriate next steps (likely a PATCH to add the failed ingredients correctly)


Swagger available on http://localhost:5000/swagger-ui
