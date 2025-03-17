from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.concurrency import asynccontextmanager
import uvicorn
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()
POOL = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global POOL
    POOL = ProcessPoolExecutor(max_workers=1)
    yield
    ...


hotels: list[dict[str, str | int]] = [
    {"id": 1, "title": "Hotel A", "name": "A"},
    {"id": 2, "title": "Hotel B", "name": "B"},
    {"id": 3, "title": "Hotel C", "name": "C"},
]


@app.get("/hotels")
def get_hotels(
    title: str | None = Query(description="Title", default=None),
    id: int | None = Query(description="id", default=None),
):
    if not title and not id:
        return hotels
    _hotels = []
    for h in hotels:
        if title and title == h["title"]:
            _hotels.append(h)
        if id and id == h["id"]:
            _hotels.append(h)
    return _hotels


@app.delete("/hotels/{hotel_id}")
def delete_hotel(
    hotel_id: int,
):
    for h in hotels:
        if hotel_id == h["id"]:
            hotels.remove(h)
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),
):
    id = int(hotels[-1]["id"]) + 1
    hotels.append({"id": id, "title": title, "name": ""})
    return hotels[-1]


# patch, put
@app.patch("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str | None = Body(),
    name: str | None = Body(),
):
    for h in hotels:
        if hotel_id == h["id"]:
            if title:
                h["title"] = title
            if name:
                h["name"] = name
            return h
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/hotels/{hotel_id}")
def rewrite_hotel(
    hotel_id: int,
    title: str = Body(),
    name: str = Body(),
):
    for h in hotels:
        if hotel_id == h["id"]:
            h["title"] = title
            h["name"] = name
            return h
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9000)
