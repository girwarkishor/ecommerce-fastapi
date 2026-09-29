# ecommerce-fastapi

Start Valkey with `docker compose up -d valkey`. When FastAPI runs directly in
the Codespace, it connects using `REDIS_URL=redis://localhost:6379/0` (the
default). Check the connection at `http://localhost:8000/health/redis` while
the FastAPI development server is running. If FastAPI is later added as a
Compose service, use `REDIS_URL=redis://valkey:6379/0` instead.

## Valkey

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

# 1. Initialize modern non-packaged project
$ uv init --no-package

# 2. Add Core Production Dependencies
uv add "fastapi[standard]" "pydantic-settings>=2.0" "sqlalchemy[asyncio]>=2.0" "asyncpg>=0.29" "alembic>=1.13" "passlib[bcrypt]>=1.7" "python-jose[cryptography]>=3.3" "python-multipart>=0.0.9" "redis>=5.0" "aiofiles>=23.2"

| Package | Role 
| --- | ---
| fastapi[standard] | Web framework + tooling
| pydantic-settings | Config from .env 
| sqlalchemy[asyncio] | Async ORM 
| asyncpg | Async Postgres driver
| alembic | DB migrations
| passlib[bcrypt] | Password hashing 
| python-jose | JWT auth
| python-multipart | File uploads / forms
| redis | Caching / rate-limit
| aiofiles | Async file writing

# 3. Add Development & Testing Dependencies
uv add --dev pytest pytest-asyncio httpx greenlet

| Package | Role | Why you need it |
| --- | --- | --- |
| pytest | Test Runner | To run your tests and check for bugs. |
| pytest-asyncio | Async Bridge | To allow pytest to run async def test functions. |
| httpx | HTTP Client | To send fake "GET/POST" requests to your API during testing. |
| greenlet | Support Library | Required by SQLAlchemy to make async database calls work. |

# 4. Run Development Server with Auto-Reload
uv run fastapi dev app/main.py

You can check Valkey in two ways:

Check the service itself:


A healthy service replies PONG.

Check the FastAPI app’s connection:


Expect {"status":"ok","service":"valkey"}. Start the app first with uv run fastapi dev app/main.py if it isn’t already running.

For a quick read/write check:


The second command should return hello.