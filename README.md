# User Management REST API

A containerized REST API for managing users, built with **FastAPI**,
**SQLAlchemy**, and **SQLite**. The project was developed as a hands-on
exercise in building a backend service from scratch and taking it
through testing, database migrations, configuration management, Docker,
and deployment.

> **Live demo:**
> `https://fastapi-user-management-6r75.onrender.com`\
> **Interactive API documentation:**
> `https://fastapi-user-management-6r75.onrender.com/docs#/`\

## Table of contents

-   [Project overview](#project-overview)
-   [Goals and learning outcomes](#goals-and-learning-outcomes)
-   [Technology stack](#technology-stack)
-   [Architecture and request flow](#architecture-and-request-flow)
-   [Project structure](#project-structure)
-   [API reference](#api-reference)
-   [Configuration](#configuration)
-   [Run locally](#run-locally)
-   [Database migrations with
    Alembic](#database-migrations-with-alembic)
-   [Testing](#testing)
-   [Docker](#docker)
-   [Deployment to Render](#deployment-to-render)
-   [SQLite persistence](#sqlite-persistence)
-   [Common commands](#common-commands)
-   [Design decisions and
    limitations](#design-decisions-and-limitations)

## Project overview

This application provides CRUD (Create, Read, Update, Delete) operations
for user records through a REST API.

It is more than a set of endpoints. The project also demonstrates how
to:

-   Organize a FastAPI application into routes, services, database
    models, and validation schemas.
-   Validate incoming data and return predictable API responses.
-   Manage database access through SQLAlchemy sessions.
-   Version database schema changes with Alembic migrations.
-   Centralize configuration in environment variables and validate it
    with Pydantic Settings.
-   Test API behavior using `pytest` and FastAPI's `TestClient`.
-   Package the application into a Docker image.
-   Deploy the container to Render and preserve SQLite data using a
    persistent disk.

## Goals and learning outcomes

The project was built to practice the full lifecycle of a small backend
service:

1.  **Application development:** implement user CRUD endpoints and
    understand how requests move through the application.
2.  **Data validation:** use Pydantic schemas to validate input and
    define response shapes.
3.  **Database access:** use SQLAlchemy ORM models, an engine, and
    sessions rather than writing database access code directly into
    routes.
4.  **Schema evolution:** use version-controlled Alembic migrations
    instead of relying on automatic table creation at application
    startup.
5.  **Testing:** cover successful operations and expected error cases.
6.  **Configuration:** load settings from environment variables or a
    local `.env` file, with validation.
7.  **Containerization:** build and run the same application in Docker.
8.  **Deployment and persistence:** deploy to Render and keep the SQLite
    database on persistent storage instead of the container's ephemeral
    filesystem.

## Technology stack

  -----------------------------------------------------------------------
  Technology              Purpose                 Why it is used
  ----------------------- ----------------------- -----------------------
  Python 3.12             Application language    Backend implementation
                                                  and ecosystem

  FastAPI                 Web/API framework       Defines routes, request
                                                  handling, dependency
                                                  injection, and
                                                  automatic OpenAPI
                                                  documentation

  Uvicorn                 ASGI server             Runs the FastAPI
                                                  application

  Pydantic                Data validation and     Validates request data
                          serialization           and shapes API
                                                  responses

  Pydantic Settings       Configuration           Loads settings from
                          management              environment variables
                                                  and `.env`, and
                                                  validates configuration

  SQLAlchemy ORM          Database toolkit and    Maps Python models to
                          ORM                     database tables and
                                                  manages database
                                                  connections and
                                                  sessions

  SQLite                  Database                Simple file-based
                                                  database for local
                                                  development and this
                                                  single-instance
                                                  deployment

  Alembic                 Database migrations     Versions schema changes
                                                  and applies or reverses
                                                  migrations

  pytest                  Test runner             Runs automated tests

  FastAPI `TestClient`    API testing             Sends test requests to
                                                  the app without
                                                  requiring a separately
                                                  running server

  Docker                  Containerization        Packages the
                                                  application and its
                                                  dependencies into a
                                                  reproducible image

  Render                  Hosting/deployment      Builds and runs the
                                                  Dockerized web service

  Render Persistent Disk  Persistent file storage Stores the SQLite
                                                  database outside the
                                                  replaceable container
                                                  filesystem

  Git / GitHub            Version control and     Tracks changes and
                          source hosting          provides the source
                                                  repository for
                                                  deployment
  -----------------------------------------------------------------------

### Important terminology

-   **SQLAlchemy** is the database toolkit/ORM used by the application.
-   **Alembic** is the database migration tool. It tracks schema changes
    in migration scripts.
-   **Pydantic Settings** manages and validates application
    configuration.
-   **SQLite** is the database engine; `users.db` is the database file.
-   **Docker** packages the application; it does not by itself provide
    persistent storage.
-   **Render Persistent Disk** stores the SQLite file outside the
    container's ephemeral filesystem.

## Architecture and request flow

A typical request follows this path:

1.  The client sends an HTTP request to a FastAPI endpoint.
2.  FastAPI validates the request using the relevant Pydantic schema.
3.  The route calls the appropriate service/business logic.
4.  The service uses SQLAlchemy and a database session to read or modify
    a user record.
5.  The result is serialized using the response schema.
6.  FastAPI returns an HTTP response with the appropriate status code.

Database schema changes follow a separate path: Alembic reads the
migration configuration and applies pending migration scripts to the
configured database.

### Main responsibilities

-   **Routes:** HTTP methods, paths, request/response handling, and
    status codes.
-   **Services:** CRUD operations and application logic.
-   **SQLAlchemy models:** database table and column definitions.
-   **Pydantic schemas:** request validation and response serialization.
-   **Database session module:** engine, session factory, and connection
    configuration.
-   **Configuration module:** validated settings shared by FastAPI,
    SQLAlchemy, and Alembic.
-   **Alembic migrations:** versioned database schema changes.

## Project structure

The following is the logical structure of the application. Exact
filenames may differ slightly depending on the final repository.

``` text
.
├── app/
│   ├── main.py                 # FastAPI app and health endpoint
│   ├── core/
│   │   └── config.py           # Validated environment-based settings
│   ├── api/
│   │   └── routes/
│   │       └── users.py        # User API routes
│   ├── services/               # User CRUD/business logic
│   ├── models/
│   │   └── user.py             # SQLAlchemy UserDB model
│   ├── schemas/                # Pydantic request/response schemas
│   └── db/
│       ├── base.py             # SQLAlchemy declarative Base
│       └── session.py          # Engine and SessionLocal
├── alembic/
│   ├── env.py                  # Alembic metadata and DB configuration
│   └── versions/               # Version-controlled migration scripts
├── tests/                      # pytest test suite
├── .env.example                # Safe configuration template
├── .gitignore                  # Excludes local files and secrets
├── .dockerignore               # Excludes files from Docker build context
├── Dockerfile                  # Container image definition
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
└── README.md
```

## API reference

FastAPI generates interactive documentation automatically. Once the
application is running, use:

-   Swagger UI: `/docs`
-   ReDoc: `/redoc`
-   OpenAPI schema: `/openapi.json`

For a deployed service, prepend the live base URL to these paths.

### API Endpoints

The paths below reflect the routes implemented during development.
Confirm the update and delete HTTP methods against `/docs` if they
differ in the final code.

| Method | Endpoint | Purpose | Typical Success Response |
|--------|----------|---------|--------------------------|
| `GET` | `/health` | Check whether the API is responding | `200 OK` |
| `POST` | `/users/new` | Create a user | `201 Created` |
| `GET` | `/users/all` | Return all users | `200 OK` |
| `GET` | `/users/{user_id}` | Retrieve one user by ID | `200 OK` |
| `PUT` | `/users/{user_id}` | Update a user | `200 OK` |
| `DELETE` | `/users/{user_id}` | Delete a user | `204 No Content` |


The collection endpoint `/users/all` is declared before the dynamic
`/users/{user_id}` route so that the literal path `all` is not
interpreted as a user ID.

### Health check

**Request**

``` http
GET /health
```

**Example response**

``` json
{
  "status": "ok",
  "statusCode": 200
}
```

### Create a user

**Request**

``` http
POST /users/new
Content-Type: application/json
```

**Example request body**

``` json
{
  "name": "Moinul Ali",
  "email": "moinul@example.com"
}
```

If the final request schema includes `phone_number`, it may be supplied
as well:

``` json
{
  "name": "Moinul Ali",
  "email": "moinul@example.com",
  "phone_number": "+919876543210"
}
```

**Expected behavior**

-   A valid request creates a user.
-   A duplicate email returns `409 Conflict`.
-   Invalid request data returns `422 Unprocessable Entity`.
-   The response body follows the configured user response schema.

### List users

**Request**

``` http
GET /users/all
```

Returns the user collection using the response schema configured by the
application. Pagination has not been documented as implemented; if added
later, document its query parameters here.

### Retrieve a user

**Request**

``` http
GET /users/{user_id}
```

Replace `{user_id}` with the user's database ID. The response should
return the matching user or the application's not-found response when
the ID does not exist.

### Update a user

**Request**

``` http
PUT /users/{user_id}
```

Use the HTTP method exposed by the final route (`PUT` or `PATCH`).
Provide the fields accepted by the update schema. Verify whether the
endpoint expects all fields or supports partial updates in `/docs`.

### Delete a user

**Request**

``` http
DELETE /users/{user_id}
```

Deletes the matching user. Check the actual route's configured status
code and response body in `/docs`.

### Error responses

  Status                       Meaning in this API
  ---------------------------- ---------------------------------------------
  `200 OK`                     Request succeeded
  `201 Created`                User created
  `204 No Content`             Possible successful deletion, if configured
  `404 Not Found`              Requested user does not exist
  `409 Conflict`               Duplicate email
  `422 Unprocessable Entity`   Request validation failed

The exact success status for update/delete depends on the route
implementation. The interactive OpenAPI documentation is the source of
truth for the running application.

## Configuration

Configuration is centralized in `app/core/config.py` and loaded through
Pydantic Settings. This avoids hardcoding settings separately in the
application and Alembic.

### Environment variables

| Variable | Purpose | Local example |
|---|---|---|
| `APP_NAME` | FastAPI application title | `User Management API` |
| `DEBUG` | Enables/disables FastAPI debug mode | `false` |
| `DATABASE_URL` | SQLAlchemy database connection URL | `sqlite:///./users.db` |


Example `.env` file:

``` dotenv
APP_NAME="User Management API"
DEBUG=false
DATABASE_URL="sqlite:///./users.db"
```

Create a local `.env` from `.env.example`. Do not commit `.env` or real
credentials to source control.

### Configuration validation

The settings module validates configuration at load time. For example,
the database URL is parsed and checked against supported database
drivers. Missing or malformed required configuration should fail early
instead of silently choosing an unintended database.

Validation of the URL's format does not prove that the database is
reachable or that credentials are correct; connection failures occur
when the application connects.

### SQLite URL formats

Local development:

``` text
sqlite:///./users.db
```

This points to a relative database file under the application's working
directory.

Render persistent disk:

``` text
sqlite:////var/data/users.db
```

This points to an absolute path on the mounted persistent disk. The
directory must exist and be writable by the service process.

## Run locally

### 1. Requirements

-   Python 3.12
-   Git
-   A terminal
-   Optional: Docker for containerized execution

### 2. Clone and enter the repository

``` bash
git clone <GITHUB_REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

Replace the placeholders with the actual repository URL and directory.

### 3. Create and activate a virtual environment

macOS/Linux:

``` bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

``` bash
cp .env.example .env
```

Review `.env` and ensure `DATABASE_URL` points to the intended local
database.

### 6. Apply migrations

``` bash
python -m alembic upgrade head
```

This creates the database schema using the migration history. The
application should not need to call `Base.metadata.create_all()` at
startup.

### 7. Start the API

``` bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore and test the API.

## Database migrations with Alembic

Alembic manages schema changes as version-controlled Python files. Each
migration contains an `upgrade()` function and a `downgrade()` function.

### Current migration sequence

The project has these migrations:

1.  `91633342cf5a` --- creates the initial `users` table.
2.  `b085c78f0f5f` --- adds the nullable `phone_number` column.

The initial migration was corrected to create the base schema. A
temporary fresh SQLite database was then used to verify that running all
migrations creates the expected table and columns.

### Common commands

Check the current database revision:

``` bash
python -m alembic current
```

Show migration history:

``` bash
python -m alembic history
```

Generate a migration by comparing model metadata with the database:

``` bash
python -m alembic revision --autogenerate -m "describe schema change"
```

Inspect the generated file before applying it. Autogenerate is a
proposal, not a substitute for reviewing the migration.

Apply all pending migrations:

``` bash
python -m alembic upgrade head
```

Revert one migration:

``` bash
python -m alembic downgrade -1
```

Check whether model metadata differs from the database schema:

``` bash
python -m alembic check
```

**Important:** A downgrade can drop columns or tables and destroy stored
data. Back up important databases before applying migrations or
downgrades. Do not edit already-shared migration history casually;
coordinate changes when other environments may have applied it.

## Testing

The project uses `pytest` and FastAPI's `TestClient`.

Run the test suite:

``` bash
python -m pytest -v
```

Use `python -m pytest` if invoking `pytest` directly does not resolve
the same Python environment on your machine.

Tests developed for the project cover API behavior such as:

-   Successful user creation.
-   Duplicate email handling (`409`).
-   Invalid request validation (`422`).
-   Retrieving all users.
-   Retrieving, updating, and deleting users.

The test suite uses an isolated SQLite database so tests do not need to
modify the development database. Keep test database setup independent
from the deployed database.

## Docker

Docker packages the application and its Python dependencies into an
image. This helps keep the runtime environment consistent between local
development and deployment.

### Build the image

``` bash
docker build -t user-management-api .
```

### Run with a persistent Docker volume

Create a named volume:

``` bash
docker volume create user-api-data
```

Run the container:

``` bash
docker run --name user-api \
  -p 8000:10000 \
  -e DATABASE_URL=sqlite:////var/data/users.db \
  -e APP_NAME="User Management API" \
  -e DEBUG=false \
  -v user-api-data:/var/data \
  user-management-api
```

Test:

-   `http://localhost:8000/health`
-   `http://localhost:8000/docs`

The container listens on port `10000`; the command maps it to port
`8000` on the host.

To remove the container:

``` bash
docker rm -f user-api
```

The named volume remains after container removal. Starting a new
container with the same volume preserves the database file. Do not
remove the volume if you need its data.

### Why `.dockerignore` matters

The `.dockerignore` file prevents unnecessary or sensitive files---such
as `.env`, `.venv/`, local database files, caches, and `.git/`---from
entering the Docker build context.

## Deployment to Render

The application is deployed as a Docker-based Render web service.

### Deployment requirements

1.  Push the application, Dockerfile, dependency list, Alembic
    configuration, and migration scripts to GitHub.
2.  Create a Render Web Service connected to the repository and select
    Docker.
3.  Attach a persistent disk mounted at `/var/data`.
4.  Set the required environment variables in the Render service
    settings.
5.  Deploy and verify the health endpoint, CRUD routes, logs, and
    database persistence.

### Production environment variables

``` text
APP_NAME=User Management API
DEBUG=false
DATABASE_URL=sqlite:////var/data/users.db
```

Configure these in Render rather than baking them into the Docker image.

### Migrations during startup

The container start command runs:

``` bash
alembic upgrade head
```

before starting Uvicorn. This applies pending migrations against the
configured runtime database.

For this single-instance SQLite setup, deploy migrations in a
coordinated way and back up the database before schema changes. Do not
run concurrent migration processes against the same SQLite file.

### Health verification

After deployment, verify:

-   `https://YOUR-SERVICE.onrender.com/health`
-   `https://YOUR-SERVICE.onrender.com/docs`
-   User creation and retrieval.
-   Data persistence after a redeploy or service restart.

Replace `YOUR-SERVICE` with the actual Render hostname.

## SQLite persistence

A container's ordinary writable filesystem is ephemeral. Data written
only inside the container can be lost when the container is replaced or
redeployed.

This project keeps SQLite by placing the database file on a persistent
disk:

``` text
DATABASE_URL=sqlite:////var/data/users.db
```

The `/var/data` path must match the Render disk mount path.

### What this approach provides

-   The SQLite database file can survive container replacement and
    service redeployments.
-   The application can retain the existing SQLite SQLAlchemy driver.
-   No separate database server is required for this small learning
    project.

### Limitations

-   A Render persistent disk is associated with one service instance;
    this setup is not appropriate for horizontally scaling multiple API
    instances.
-   SQLite has different concurrency characteristics from a
    client-server database.
-   Persistent storage is not a backup strategy. Keep backups for data
    you cannot afford to lose.
-   A local SQLite database is not automatically copied to Render. The
    deployed service creates or uses the database at its configured
    persistent path.

For a multi-instance service, higher write concurrency, or a larger
production workload, a managed PostgreSQL database is generally a better
fit. Switching is a separate architectural decision; it is not required
merely to containerize this project.

## Common commands

  ----------------------------------------------------------------------------------------------
  Task                                Command
  ----------------------------------- ----------------------------------------------------------
  Install dependencies                `python -m pip install -r requirements.txt`

  Run locally                         `uvicorn app.main:app --reload`

  Run tests                           `python -m pytest -v`

  Current Alembic revision            `python -m alembic current`

  Migration history                   `python -m alembic history`

  Apply migrations                    `python -m alembic upgrade head`

  Create migration                    `python -m alembic revision --autogenerate -m "message"`

  Check schema differences            `python -m alembic check`

  Build Docker image                  `docker build -t user-management-api .`
  ----------------------------------------------------------------------------------------------

## Design decisions and limitations

### Why FastAPI?

FastAPI provides typed request handling, dependency injection, and
automatic OpenAPI documentation with relatively little boilerplate.

### Why SQLAlchemy?

SQLAlchemy separates database operations from HTTP route handling and
provides a consistent ORM/database toolkit. It also allows the database
URL to be supplied through configuration.

### Why Alembic instead of automatic table creation?

Versioned migrations make schema changes reviewable, repeatable, and
suitable for deployment. Automatic table creation during application
startup can hide schema-management problems and does not replace a
migration history.

### Why environment-based configuration?

The same application image can run locally and in deployment
environments with different database URLs and settings. Configuration
and secrets remain outside the source code.

### Why SQLite on Render?

SQLite keeps this learning project simple and demonstrates the
difference between container lifecycle and persistent data. A persistent
disk solves file persistence for a single service instance; it does not
make SQLite a horizontally scalable database.

### Current scope

This is a learning-focused CRUD API rather than a complete production
identity system. Before using it for sensitive real-world user data,
consider adding or reviewing authentication and authorization, rate
limiting, structured logging, backup and restore procedures, pagination,
monitoring, and an explicit data-retention policy.

------------------------------------------------------------------------

## Project status

Completed learning milestones:

-   FastAPI CRUD implementation.
-   Pydantic validation and response schemas.
-   SQLAlchemy database access.
-   Automated tests with pytest.
-   Alembic migrations, including fresh-database verification.
-   Reusable environment-based configuration with validation.
-   Docker image and local container testing.
-   Render deployment with a persistent SQLite storage strategy.

