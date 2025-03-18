from typing import Annotated
from pydantic import BaseModel
from fastapi import Query, Depends


class PaginationParamsSchema(BaseModel):
    page: Annotated[int, Query(description="Page", default=1, ge=1)]
    per_page: Annotated[int, Query(description="Limit", default=3, ge=1, lt=101)]


PaginationDep = Annotated[PaginationParamsSchema, Depends()]
