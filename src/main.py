import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.rooms import router as rooms_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(users_router)
app.include_router(rooms_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
