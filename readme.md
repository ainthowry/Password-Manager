This repo uses pipenv to handle dependencies in lock environment

Using Deta to deploy the backend and Railway to deploy the DB

DB: Postgresql, Backend: Fastapi, ORM: SQLAlchemy

Libs used: asynpc, pycryptodome, secrets, sqlalchemy, passlib

To re-generate requirements.txt after updating dependencies, run the following command (you need to make sure the encoding of the requirements.txt is utf-8)

```
pipenv run pip freeze > requirements.txt
```
