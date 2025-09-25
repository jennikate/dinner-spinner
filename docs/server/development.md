# Development

## Adding packages

We are currently using pip/requirements for this project as it's quite small.

To add a package
```bash
pip install <package-name>
```

And then update requirements.txt
```bash
pip freeze > requirements.txt
```

You may want to then move any dev only requirements into requirements-dev.txt so they're not unnecessarily loaded into production.

## Database migrations

We're running SQLite in a specified location (/src/app/datbase.db).

To recreate the database clean (e.g. you deleted the old file) `flask db init`

To create migration `flask db migrate -m "Initial migration."` or whatever relevant name

To set migration `flask db upgrade`
