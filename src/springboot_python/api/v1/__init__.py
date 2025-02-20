from fastapi import APIRouter

from springboot_python.api.v1.student import router as StudentRouter


__all__ = (
    StudentRouter,
)


router = APIRouter()


for api_router in __all__:
    router.include_router(api_router)