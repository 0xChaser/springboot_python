from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    author: str
    title: str
    
    model_config=ConfigDict(from_attributes=True)

class BookIn(BookBase):
    pass

class BookOut(BookIn):
    id: UUID

class BookPatch(BookIn):
    pass