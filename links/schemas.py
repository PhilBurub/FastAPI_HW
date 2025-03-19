from pydantic import BaseModel
from typing import Union
from datetime import datetime


class StatusResponse(BaseModel):
    status: str


class CredentialHeader(BaseModel):
    login: str
    token: str = None


class Link(BaseModel):
    url: str
    alias: str = None
    created: datetime = None
    last_accessed: Union[datetime, None] = None
    times_accessed: int = 0
    expires_at: Union[datetime, None] = None


class ResponseRegister(BaseModel):
    message: str
    content: CredentialHeader


class ResponseAlias(BaseModel):
    message: str
    content: Link
