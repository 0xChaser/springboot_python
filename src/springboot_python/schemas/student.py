from uuid import UUID
from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    name: str

    model_config=ConfigDict(from_attributes=True)

class StudentIn(StudentBase):
    pass

class StudentOut(StudentIn):
    id: UUID

class StudentPatch(StudentIn):
    pass