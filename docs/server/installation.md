# Installing Server

Make sure you are in the `server` folder.

1. Create a virtual environment

```bash
python -m venv venv
```

2. Activate the environment

```bash
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

or requirements.txt for prod

4. Create a .env file at the top level of the project
Make sure you do NOT create it within /server
The .env file contains variables for both server and client so lives at the top

e.g.
dinner-spinner
|_client
|_design
|_docs
|_server
|_.env

```bash

```

run 
```bash
source .env
```

5. Run migrations
As it is running on SQLite on your local device for now you need to 

a. make sure you are in the `server` folder
b. run `flask db upgrade`


5. Run the app
TODO: replace this with a script to run both BE and FE

For now, return to `/server` folder and `python src/run.py`
