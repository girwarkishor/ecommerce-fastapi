from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.redis import create_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis_client = create_redis_client()
    app.state.redis = redis_client
    try:
        yield
    finally:
        await redis_client.aclose()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/health/redis")
async def redis_health(request: Request) -> dict[str, str]:
    try:
        await request.app.state.redis.ping()
    except RedisError as exc:
        raise HTTPException(status_code=503, detail="Valkey is unavailable") from exc
    return {"status": "ok", "service": "valkey"}

def main():
    print("Hello from ecommerce-fastapi!")


if __name__ == "__main__":
    main()
