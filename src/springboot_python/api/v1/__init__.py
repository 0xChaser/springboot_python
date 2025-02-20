from fastapi import APIRouter

from springboot_python.api.v1.student import router as StudentRouter
from springboot_python.api.v1.book import router as BookRouter


__all__ = (
    StudentRouter,
    BookRouter,
)


router = APIRouter()


for api_router in __all__:
    router.include_router(api_router)