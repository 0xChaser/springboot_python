from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from springboot_python.daos.base import BaseDao
from springboot_python.exceptions.book import BookLinkedToAnotherObject
from springboot_python.models.book import Book

class BookDao(BaseDao):

    def __init__(self, session:AsyncSession):
        super().__init__(session)

    async def create(self, book_data: dict) -> Book:
        _book = Book(**book_data)
        self.session.add(_book)
        await self.session.commit()
        await self.session.refresh(_book)
        return _book
    
    async def get_by_id(self, book_id: UUID) -> Book | None:
        statement = select(Book).where(Book.id == book_id)
        return await self.session.scalar(statement=statement)

    async def get_all(self, offset:int, limit:int) -> list[Book]:
        statement = select(Book).offset(offset).limit(limit)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    async def delete_by_id(self, book_id:UUID) -> None:
        _book = await self.get_by_id(book_id=book_id)
        try:
            statement = delete(Book).where(Book.id == book_id)
            await self.session.execute(statement=statement)
            await self.session.commit()
        except IntegrityError:
            raise BookLinkedToAnotherObject
        return _book
    
    async def count(self) -> int:
        statement = select(func.count()).select_from(Book)
        result = await self.session.execute(statement=statement)
        return result.scalar_one()