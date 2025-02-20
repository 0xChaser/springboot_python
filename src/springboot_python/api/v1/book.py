from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from springboot_python.db import get_session
from springboot_python.schemas.book import (
    BookIn,
    BookOut,
    BookPatch
)
from springboot_python.schemas.page import Page
from springboot_python.services.book import BookService

router = APIRouter(prefix="/book", tags=["Book"])

@router.get("/", response_model=Page[BookOut])
async def list_book(
    offset:int=0,
    limit:int=10,
    session:AsyncSession = Depends(get_session)
):
    """
    Get all book:
    
    Return : 
    
    BookOut : Book with all it's attributes (id, title,...) 
    
    """
    return await BookService.get_all_book(session=session, offset=offset, limit=limit)

@router.get("/{id}", response_model=BookOut)
async def get_book(id:UUID, session:AsyncSession=Depends(get_session)):
    return await BookService.get_by_id(id, session)


@router.post("/")
async def add_book(book_data:BookIn, session:AsyncSession=Depends(get_session)):
    return await BookService.add_book(book_data, session)

@router.patch("/{id}", response_model=BookOut)
async def update_book(id:UUID, book:BookPatch, session:AsyncSession=Depends(get_session)):
    return await BookService.update_by_id(id, book, session)

@router.delete("/{id}", response_model=BookOut)
async def delete_book(id:UUID,session:AsyncSession=Depends(get_session)):
    return await BookService.delete_by_id(id, session)