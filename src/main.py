from contextlib import asynccontextmanager
import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facility_router
from src.api.images import router as image_router
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app...")
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    print("Closing app...")
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facility_router)
app.include_router(image_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
