from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from springboot_python.daos import book
from springboot_python.exceptions.book import BookNotFound
from springboot_python.schemas.book import BookIn, BookOut, BookPatch
from springboot_python.schemas.page import Page


class BookService:

    @staticmethod
    async def add_book(book_data:BookIn, session:AsyncSession):
        new_book = await book.BookDao(session).create(book_data.model_dump())
        logger.info(f"New Book created successfully: {new_book}")
        return new_book
    
    @staticmethod
    async def get_all_book(offset:int, limit:int, session:AsyncSession) -> Page[BookOut]:
        all_book = await book.BookDao(session).get_all(offset=offset, limit=limit)
        return Page(
            total = await book.BookDao(session).count(),
            items=[BookOut.model_validate(_book) for _book in all_book],
            offset=offset,
            limit=limit,
        )
    
    @staticmethod
    async def get_by_id(book_id:UUID, session:AsyncSession) -> BookOut | None :
        _book = await book.BookDao(session).get_by_id(book_id)
        if not _book:
            raise BookNotFound
        return _book
    
    @staticmethod
    async def update_by_id(book_id: UUID, book_patch:BookPatch, session:AsyncSession) -> BookPatch:
        _book = await book.BookDao(session).get_by_id(book_id)
        if not _book:
            raise BookNotFound
        for key,value in book_patch.model_dump(exclude_unset=True).items():
            setattr(_book, key, value)
        await session.commit()
        return _book
    
    @staticmethod
    async def delete_by_id(book_id:UUID, session:AsyncSession) -> None:
        _book = await book.BookDao(session).delete_by_id(book_id)
        if not _book:
            raise BookNotFound
        return _book
