from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from springboot_python.daos.base import BaseDao
from springboot_python.exceptions.student import StudentLinkedToAnotherObject
from springboot_python.models.student import Student

class StudentDao(BaseDao):

    def __init__(self, session:AsyncSession):
        super().__init__(session)

    async def create(self, student_data: dict) -> Student:
        _student = Student(**student_data)
        self.session.add(_student)
        await self.session.commit()
        await self.session.refresh(_student)
        return _student
    
    async def get_by_id(self, student_id: UUID) -> Student | None:
        statement = select(Student).where(Student.id == student_id)
        return await self.session.scalar(statement=statement)

    async def get_all(self, offset:int, limit:int) -> list[Student]:
        statement = select(Student).offset(offset).limit(limit)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    async def delete_by_id(self, student_id:UUID) -> None:
        _student = await self.get_by_id(student_id=student_id)
        try:
            statement = delete(Student).where(Student.id == student_id)
            await self.session.execute(statement=statement)
            await self.session.commit()
        except IntegrityError:
            raise StudentLinkedToAnotherObject
        return _student
    
    async def count(self) -> int:
        statement = select(func.count()).select_from(Student)
        result = await self.session.execute(statement=statement)
        return result.scalar_one()