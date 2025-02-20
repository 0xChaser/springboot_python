import uuid 

from sqlalchemy import UUID, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from springboot_python.models.base import Base

class Student(Base):
    
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False, primary_key=True
    )

    name: Mapped[str] = mapped_column(String(), nullable=False)

    