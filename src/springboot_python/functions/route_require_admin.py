from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer


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
