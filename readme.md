This repo uses pipenv to handle dependencies in lock environment

- Using Heroku to deploy the backend and Railway to deploy the DB
  <br>

- DB: **Postgresql**
- Backend: **Fastapi**
- ORM: **SQLAlchemy**

Additional libs used: **asynpc, sqlalchemy, secrets, passlib, bcrypt, pycryptodome** (Refer to pipfile)

To re-generate requirements.txt after updating dependencies, run the following command

```
pipenv run pip freeze > requirements.txt
```

Heroku requires 3 files to deploy: procfile, requirements.txt and runtime.txt (examples provided)

To deploy this locally, simply start up the venv then run main.py

```
pipenv install

pipenv shell

py main.py
```
