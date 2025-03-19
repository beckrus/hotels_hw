import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router

app = FastAPI()
POOL = None


app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9000)
