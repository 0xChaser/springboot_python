from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class StudentBase(BaseModel):
    name: str
    email: EmailStr

    model_config=ConfigDict(from_attributes=True)

class StudentIn(StudentBase):
    pass

class StudentOut(StudentIn):
    id: UUID

class StudentPatch(StudentIn):
    pass