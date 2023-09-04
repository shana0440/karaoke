from pydantic import BaseModel
from sqlalchemy.orm import Query
from schemas.pagination import PaginationSchema


def paginate(query: Query, limit: int, offset: int, schema: BaseModel):
    total = query.count()
    data = query.limit(limit).offset(offset)
    return PaginationSchema(
        total=total,
        limit=limit,
        offset=offset,
        data=[schema.model_validate(it) for it in data],
    )
