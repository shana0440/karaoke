from pydantic import BaseModel
from typing import Any, List


class PaginationSchema(BaseModel):
    total: int
    offset: int
    limit: int
    data: List[Any]
