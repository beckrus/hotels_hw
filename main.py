from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn
from concurrent.futures import ProcessPoolExecutor

from hotels import router as hotels_router

app = FastAPI()
POOL = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global POOL
    POOL = ProcessPoolExecutor(max_workers=1)
    yield
    ...


app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9000)
