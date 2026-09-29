# ecommerce-fastapi

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