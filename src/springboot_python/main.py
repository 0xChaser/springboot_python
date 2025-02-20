from importlib.metadata import version

from fastapi import FastAPI, Request, status, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from springboot_python.controller import AuthController
from springboot_python.api.v1 import router
from springboot_python.models.keycloak import TokenResponse, UserInfo

app = FastAPI(
    title="KeyCloak Python",
    version=version(__package__),
    root_path="/api/v1",
    )

bearer_scheme = HTTPBearer()

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


# Define the root endpoint
@app.get("/")
async def read_root():
    """
    Root endpoint that provides a welcome message and documentation link.
    """
    return AuthController.read_root()


# Define the login endpoint
@app.post("/login", response_model=TokenResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Login endpoint to authenticate the user and return an access token.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user.

    Returns:
        TokenResponse: Contains the access token upon successful authentication.
    """
    return AuthController.login(username, password)


# Define the protected endpoint
@app.get("/protected", response_model=UserInfo)
async def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Protected endpoint that requires a valid token for access.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

    Returns:
        UserInfo: Information about the authenticated user.
    """
    return AuthController.protected_endpoint(credentials)
