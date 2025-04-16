from contextlib import asynccontextmanager
import sys
from pathlib import Path
import logging

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facility_router
from src.api.images import router as image_router
from src.api.status import router as status_router
from src.init import redis_manager
from src.config import settings


FORMAT = "%(asctime)s::%(levelname)s::%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%d/%m/%Y %I:%M:%S")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app...")
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cahce initialized")
    yield
    logging.info("Closing app...")
    await redis_manager.close()


# if settings.MODE == 'TEST':
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan, title="Bookings")


app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facility_router)
app.include_router(image_router)
app.include_router(status_router)

if __name__ == "__main__":
    uv_settings = {
        "app":"main:app", "reload":True, "host":"0.0.0.0", "port":8000
    }
    if settings.MODE == "PROD":
        uv_settings['reload'] = False
    uvicorn.run(**uv_settings)
