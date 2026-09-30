# ecommerce-fastapi

## Project Setup

### Initialize a Modern Non-Packaged Project

```sh
uv init --no-package
```

### Add Core Production Dependencies

```sh
uv add "fastapi[standard]" "pydantic-settings>=2.0" "sqlalchemy[asyncio]>=2.0" "asyncpg>=0.29" "alembic>=1.13" "passlib[bcrypt]>=1.7" "python-jose[cryptography]>=3.3" "python-multipart>=0.0.9" "redis>=5.0" "aiofiles>=23.2"
```

| Package | Role |
| --- | --- |
| `fastapi[standard]` | Web framework and tooling |
| `pydantic-settings` | Configuration from `.env` |
| `sqlalchemy[asyncio]` | Async ORM |
| `asyncpg` | Async PostgreSQL driver |
| `alembic` | Database migrations |
| `passlib[bcrypt]` | Password hashing |
| `python-jose` | JWT authentication |
| `python-multipart` | File uploads and forms |
| `redis` | Caching and rate limiting |
| `aiofiles` | Async file writing |

### Add Development and Testing Dependencies

```sh
uv add --dev pytest pytest-asyncio httpx greenlet
```

| Package | Role | Why you need it |
| --- | --- | --- |
| `pytest` | Test runner | To run your tests and check for bugs. |
| `pytest-asyncio` | Async bridge | To allow pytest to run async `def` test functions. |
| `httpx` | HTTP client | To send fake GET/POST requests to your API during testing. |
| `greenlet` | Support library | Required by SQLAlchemy to make async database calls work. |

### Run the Development Server

Run the server with auto-reload:

```sh
uv run fastapi dev app/main.py
```

## PostgreSQL

### Start the Service

Start PostgreSQL and Valkey from the project directory:

```sh
docker compose up -d postgres valkey
```

Wait until PostgreSQL is healthy, then verify it accepts connections:

```sh
docker compose ps
docker compose exec postgres pg_isready -U postgres -d ecommerce_db
```

`pg_isready` should report that the server is accepting connections. To run a
test query:

```sh
docker compose exec postgres psql -U postgres -d ecommerce_db -c 'SELECT 1;'
```

### Connection URL

For FastAPI running directly in the Codespace, use
`postgresql+asyncpg://postgres:postgres_password@localhost:5432/ecommerce_db`.
This is the default `DATABASE_URL` in the app and `.env.example`. For an app
running in the same Compose project, use
`postgresql+asyncpg://postgres:postgres_password@postgres:5432/ecommerce_db`.

### Data Persistence

PostgreSQL data is stored in the `postgres_data` Docker volume and remains when
the container is stopped or recreated. Stop the services with
`docker compose down`; avoid `docker compose down -v` unless you intend to
delete the database data.

## Valkey

### Start and Connect

Start Valkey with `docker compose up -d valkey`. When FastAPI runs directly in
the Codespace, it connects using `REDIS_URL=redis://localhost:6379/0` (the
default). Check the connection at `http://localhost:8000/health/redis` while
the FastAPI development server is running. If FastAPI is later added as a
Compose service, use `REDIS_URL=redis://valkey:6379/0` instead.

### Verify the Connection

You can check Valkey in two ways:

#### Check the Service

A healthy service replies `PONG`.

#### Check the FastAPI Application

Expect `{"status":"ok","service":"valkey"}`. Start the app first with
`uv run fastapi dev app/main.py` if it isn’t already running.

For a quick read/write check:

The second command should return `hello`.

### Linux Host Configuration

On Linux, Valkey recommends enabling memory overcommit on the Docker host to
avoid background-save or replication failures:

```sh
sudo sysctl -w vm.overcommit_memory=1
```

To keep the setting across reboots, add `vm.overcommit_memory = 1` to a file
such as `/etc/sysctl.d/99-valkey.conf` on the host, then apply it with
`sudo sysctl --system`. This is a host kernel setting and cannot be configured
from this Compose service.

Valkey's published port is bound to localhost; containers on the Compose
network can still connect to it using the `valkey` service name.

## Database Migrations

### Initialize Alembic

```sh
uv run alembic init -t async alembic
```

The command creates the following project structure:

```text
your-project/
├── alembic/                    ← NEW FOLDER created
│   ├── env.py                  ← Main config file (you edit this!)
│   ├── README                  ← Basic usage instructions
│   ├── script.py.mako          ← Template for new migration files
│   └── versions/               ← All your migration files go here
│       └── (empty for now)
│
├── alembic.ini                 ← NEW FILE (Alembic config)
├── app/
├── .env
└── pyproject.toml
```

One line. One run. Your entire database version control system is set up. 🚀

| Part | What It Does |
| --- | --- |
| `uv run` | Runs in your virtual environment |
| `alembic` | The migration CLI tool |
| `init` | Initialize migration system (run once!) |
| `-t async` | Use async-compatible template |
| `alembic` | Name of the folder to create |

### How Migrations Work

```text
Your Models          Alembic               Database
(Python Code)     (Migration Tool)      (Actual Tables)
     │                   │                    │
     │ 1. You change     │                    │
     │    a model        │                    │
     ├──────────────────►│                    │
     │                   │ 2. Detect changes  │
     │                   │    auto-generate   │
     │                   │    migration file  │
     │                   │                    │
     │                   │ 3. Run migration   │
     │                   ├───────────────────►│
     │                   │                    │ 4. Table
     │                   │                    │    updated!
```

### Generate a Migration

Generate a migration revision script:

```sh
uv run alembic revision --autogenerate -m "create_initial_ecommerce_tables"
```

### Apply a Migration

Apply the migration to the database:

```sh
uv run alembic upgrade head
```

### Check Migration Status

```sh
uv run alembic current
uv run alembic history --verbose
uv run alembic check
```

Check the recorded migration revision in PostgreSQL:

```sh
docker compose exec postgres psql -U postgres -d ecommerce_db \
  -c "SELECT version_num FROM alembic_version;"
```

List the database tables:

```sh
docker compose exec postgres psql -U postgres -d ecommerce_db -c '\dt'
```