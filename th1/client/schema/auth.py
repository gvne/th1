import typing as ty
import pydantic


class Request(pydantic.BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    grant_type: str = "password"


class RefreshRequest(pydantic.BaseModel):
    client_id: str
    client_secret: str
    refresh_token: str
    grant_type: str = "refresh_token"


class Response(pydantic.BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str
    legal_fault: bool
