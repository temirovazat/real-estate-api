# Real Estate API

## Technologies

```Python``` ```FastAPI``` ```PostgreSQL``` ```PyTest``` ```Docker```

## Config

* Create ".env" file and add environment variables to it:
```dotenv
# base
SECRET_KEY=some-secret-key
PROJECT_NAME='Some Project Name'
SERVER_HOST=http://0.0.0.0:8881

# databases
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_DB=postgres
POSTGRES_TEST_DB=test
PGDATA=/var/lib/postgresql/data/pgdata

# SMTP
SMTP_USER=some-email
SMTP_PASSWORD=some-password

# Auth
FIRST_SUPERUSER_USERNAME=user@user.com
FIRST_SUPERUSER_PASSWORD=password
FIRST_SUPERUSER_FIRST_NAME='first name'
FIRST_SUPERUSER_LAST_NAME='last name'
```

## Development

Run server with all dependencies:

```console
$ docker-compose up --build
```
Add pre-commit hook

```console
$ pre-commit install
```

## Tests

Testing is done with pytest, tests are placed in the "tests" directory

For testing, you should go inside the container and run the command `pytest .`

```console
$ docker exec -it <FastAPI container ID> bash
$ pytest tests --asyncio-mode=auto
```

## Migrations

* After creating the model in `app/models`, you need to import it in `app/db/base.py` (in order to make it visible to alembic)
* Make migrations (run inside container)

```console
$ alembic -n postgres revision --autogenerate -m "add column last_name to User model"
```

* Run migrations

```console
$ alembic -n postgres upgrade head
```

* Postgres
```console
$ alembic -n postgres revision --autogenerate -m "text"
$ alembic -n postgres upgrade head
$ alembic -n postgres downgrade -1
```
