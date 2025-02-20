from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from springboot_python.db import get_session
from springboot_python.schemas.student import (
    StudentIn,
    StudentOut,
    StudentPatch
)
from springboot_python.schemas.page import Page
from springboot_python.services.student import StudentService

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/", response_model=Page[StudentOut])
async def list_student(
    offset:int=0,
    limit:int=10,
    session:AsyncSession = Depends(get_session)
):
    """
    Get all student:
    
    Return : 
    
    StudentOut : Student with all it's attributes (id, name,...) 
    
    """
    return await StudentService.get_all_student(session=session, offset=offset, limit=limit)

@router.get("/{id}", response_model=StudentOut)
async def get_student(id:UUID, session:AsyncSession=Depends(get_session)):
    return await StudentService.get_by_id(id, session)


@router.post("/")
async def add_student(student_data:StudentIn, session:AsyncSession=Depends(get_session)):
    return await StudentService.add_student(student_data, session)

@router.patch("/{id}", response_model=StudentOut)
async def update_student(id:UUID, student:StudentPatch, session:AsyncSession=Depends(get_session)):
    return await StudentService.update_by_id(id, student, session)

@router.delete("/{id}", response_model=StudentOut)
async def delete_student(id:UUID,session:AsyncSession=Depends(get_session)):
    return await StudentService.delete_by_id(id, session)

@router.delete("/")
async def delete_all_student(session:AsyncSession=Depends(get_session)):
    return await StudentService.delete_all(session)