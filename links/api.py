from fastapi import APIRouter, Header
from typing import Annotated
from http import HTTPStatus
from links.schemas import CredentialHeader, Link, ResponseRegister, ResponseAlias, StatusResponse
from links.postgres import (
    register_user,
    check_user,
    add_alias,
    remove_url,
    update_url,
    stats_url
)
from string import ascii_letters, digits
from random import choices

router = APIRouter()


@router.get('/register', response_model=ResponseRegister, status_code=HTTPStatus.OK)
async def register(headers: Annotated[CredentialHeader, Header()]):
    token = ''.join(choices(ascii_letters + digits, k=10))
    if await register_user(login=headers.login, token=token):
        return ResponseRegister(content=CredentialHeader(login=headers.login, token=token), message='SUCCESS')
    else:
        return ResponseRegister(content=headers, message=f'ERROR: login {headers.login} already registered')


@router.post('/shorten', response_model=ResponseAlias, status_code=HTTPStatus.CREATED)
async def shorten(link: Link):
    meta = await add_alias(url=link.url, alias=link.alias)
    if meta.get('created'):
        return ResponseAlias(content=Link(**meta), message='SUCCESS')
    elif meta['error'] == 'alias':
        return ResponseAlias(content=link, message=f"ERROR: alias {link.alias} is already in use")
    else:
        return ResponseAlias(content=link, message=f"ERROR: alias for link {link.url} already exists")


@router.delete('/{short_code}', response_model=StatusResponse, status_code=HTTPStatus.ACCEPTED)
async def delete_url(short_code: str, headers: Annotated[CredentialHeader, Header()]):
    if await check_user(login=headers.login, token=headers.token or ""):
        if await remove_url(alias=short_code):
            return StatusResponse(status='SUCCESS')
        return StatusResponse(status=f'ERROR: alias {short_code} not found')
    return StatusResponse(status=f'ERROR: you are not registered')


@router.post('/{short_code}', response_model=ResponseAlias, status_code=HTTPStatus.CREATED)
async def post_url(short_code: str, headers: Annotated[CredentialHeader, Header()]):
    if await check_user(login=headers.login, token=headers.token or ""):
        meta = await update_url(alias=short_code)
        if meta:
            return ResponseAlias(content=Link(**meta), message='SUCCESS')
        else:
            return ResponseAlias(
                content=Link(alias=short_code, url=""),
                message=f"ERROR: link with alias {short_code} not found"
            )
    return ResponseAlias(status='ERROR: you are not registered', content=Link(url="", alias=short_code))


@router.get('/{short_code}/stats', response_model=ResponseAlias, status_code=HTTPStatus.FOUND)
async def get_stats_url(short_code: str):
    meta = await stats_url(alias=short_code)
    if meta:
        return ResponseAlias(message='SUCCESS', content=Link(**meta))
    return ResponseAlias(
        message=f'ERROR: link with alias {short_code} not found',
        content=Link(url="", alias=short_code)
    )


@router.get('/search', response_model=ResponseAlias, status_code=HTTPStatus.FOUND)
async def find_by_full_url(original_url: str):
    meta = await stats_url(url=original_url)
    if meta:
        return ResponseAlias(message='SUCCESS', content=Link(**meta))
    return ResponseAlias(
        message=f'ERROR: link {original_url} not found',
        content=Link(url=original_url)
    )
