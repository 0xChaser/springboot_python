from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from springboot_python.api.v1.student import router as StudentRouter
from springboot_python.api.v1.book import router as BookRouter

bearer_scheme = HTTPBearer()

def route_require_token(router: APIRouter) -> APIRouter:
    """
    Ajoute la dépendance 'bearer_scheme' à toutes les routes dont la méthode n'est pas GET.
    Cela oblige l'envoi d'un token dans l'en-tête Authorization.
    """
    original_routes = router.routes[:]
    router.routes.clear()

    for route in original_routes:
        if route.methods and "GET" not in route.methods:
            route.dependencies.append(Depends(bearer_scheme))
        router.routes.append(route)
    
    return router

main_router = APIRouter()

for api_router in (StudentRouter, BookRouter):
    route_require_token(api_router)
    main_router.include_router(api_router)
