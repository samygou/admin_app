from pydantic import BaseModel


class PageLimit(BaseModel):
    offset: int = 0
    size: int = 10
