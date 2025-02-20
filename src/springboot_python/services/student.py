from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from springboot_python.daos import student
from springboot_python.exceptions.student import StudentNotFound
from springboot_python.schemas.student import StudentIn, StudentOut, StudentPatch
from springboot_python.schemas.page import Page


class StudentService:

    @staticmethod
    async def add_student(Student_data:StudentIn, session:AsyncSession):
        new_Student = await student.StudentDao(session).create(Student_data.model_dump())
        logger.info(f"New Student created successfully: {new_Student}")
        return new_Student
    
    @staticmethod
    async def get_all_student(offset:int, limit:int, session:AsyncSession) -> Page[StudentOut]:
        all_Student = await student.StudentDao(session).get_all(offset=offset, limit=limit)
        return Page(
            total = await student.StudentDao(session).count(),
            items=[StudentOut.model_validate(_Student) for _Student in all_Student],
            offset=offset,
            limit=limit,
        )
    
    @staticmethod
    async def get_by_id(Student_id:UUID, session:AsyncSession) -> StudentOut | None :
        _Student = await student.StudentDao(session).get_by_id(Student_id)
        if not _Student:
            raise StudentNotFound
        return _Student
    
    @staticmethod
    async def update_by_id(Student_id: UUID, Student_patch:StudentPatch, session:AsyncSession) -> StudentPatch:
        _Student = await student.StudentDao(session).get_by_id(Student_id)
        if not _Student:
            raise StudentNotFound
        for key,value in Student_patch.model_dump(exclude_unset=True).items():
            setattr(_Student, key, value)
        await session.commit()
        return _Student
    
    @staticmethod
    async def delete_by_id(Student_id:UUID, session:AsyncSession) -> None:
        _Student = await student.StudentDao(session).delete_by_id(Student_id)
        if not _Student:
            raise StudentNotFound
        return _Student
