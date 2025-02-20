import uuid 

from sqlalchemy import UUID, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from springboot_python.models.base import Base

class Book(Base):
    
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False, primary_key=True
    )

    title: Mapped[str] = mapped_column(String(), nullable=False)
    author: Mapped[str] = mapped_column(String(), nullable=False)

    