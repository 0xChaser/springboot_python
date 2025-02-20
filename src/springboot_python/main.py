from importlib.metadata import version

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from springboot_python.api.v1 import router

app = FastAPI(
    title=__package__.replace("_", " ").title(),
    version=version(__package__),
    root_path="/api/v1",
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={exc.__class__.__name__: str(exc)})


@app.get("/", include_in_schema=False)
async def redirect_depending_user_agent(request: Request):
    return RedirectResponse("/docs")