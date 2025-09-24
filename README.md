# Dinner Spinner

Helping you decide what to cook for the week!

## Contents

Design
- [Process](/design/product-ux/README.md#process)
- [Product & UX](/design/product-ux/README.md)
- [Technical](/design/technical/README.md)

Product & Repo Structure
- [Repo structure](#repo-structure)

Version
- [Deployed](#version)
- [In Development](#version)

----

## Repo Structure

As I am not paying for hosting, the code has to be downloaded to the device you want to run it on.

It will use a local database so is not transferable across devices at this time.

It is also a product I'm documenting my processes on so it includes notes, diagrams, and commentary.

Therefore, all the code and notes are included in this one repo.

The structure is as follows.

```bash
dinner-spinner/
└── client/
├── design/
├── server/
```

**Client**: React Typescript frontendg
**Design**: process, notes, diagrams
**Server**: Flask, SQLAlchemy, Marshmallow/smorest, SQLite backend

----

## Version

**Deployed**: 0.0

**In development**: 0.1
- add and view recipes
- spin for [x] days of suggestions
- select a recipe from list to pin, then spin rest
- select a spin result to pin, then spin rest
- create list of ingredients from suggestions
