from links.models import Credentials, Links
from sqlalchemy import select, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from links.models import Base
from datetime import datetime
from typing import Dict, Union
from string import ascii_letters, digits
from random import choices
import asyncio
import nest_asyncio
nest_asyncio.apply()

DATABASE_URL = "postgresql+asyncpg://philing:postgres_password@postgres:5432"

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())


async def check_user(login: str, token: str = None) -> bool:
    async with AsyncSession(engine) as session:
        scalar = (await session.execute(select(Credentials).where(Credentials.login == login))).scalar()
        return token == scalar.token if scalar and token is not None else scalar is not None


async def register_user(login: str, token: str) -> bool:
    if not await check_user(login=login):
        async with AsyncSession(engine) as session:
            session.add(Credentials(login=login, token=token))
            await session.commit()
            return True


async def get_link(url: str = None, alias: str = None) -> Dict[str, Union[str, datetime, int]]:
    async with AsyncSession(engine) as session:
        if url:
            return (await session.execute(select(Links).where(Links.url == url))).scalar()
        if alias:
            return (await session.execute(select(Links).where(Links.alias == alias))).scalar()


async def add_alias(url: str, alias: str = None) -> Dict[str, Union[str, datetime, int]]:
    if await get_link(url=url):
        return {'url': url, 'alias': alias, 'error': 'url'}
    if alias and await get_link(alias=alias):
        return {'url': url, 'alias': alias, 'error': 'alias'}

    if not alias:
        alias = ''.join(choices(ascii_letters + digits, k=6))
        while await(get_link(alias=alias)):
            alias = ''.join(choices(ascii_letters + digits, k=6))

    async with AsyncSession(engine) as session:
        meta = {
            'url': url,
            'alias': alias,
            'created': datetime.now()
        }
        session.add(Links(**meta))
        await session.commit()
        return meta


async def find_url(alias: str):
    async with AsyncSession(engine) as session:
        meta = (await session.execute(select(Links).where(Links.alias == alias))).scalar()
        if meta:
            url = meta.url
            meta.last_accessed = datetime.now()
            meta.times_accessed += 1
            await session.commit()
            return url


async def remove_url(alias: str):
    async with AsyncSession(engine) as session:
        meta = (await session.execute(select(Links).where(Links.alias == alias))).scalar()
        if meta:
            await session.delete(meta)
            await session.flush()
            await session.commit()
            return True


async def update_url(alias: str) -> Dict[str, Union[str, datetime, int]]:
    async with AsyncSession(engine) as session:
        meta = (await session.execute(select(Links).where(Links.alias == alias))).scalar()
        if meta:
            alias = ''.join(choices(ascii_letters + digits, k=6))
            while await(get_link(alias=alias)):
                alias = ''.join(choices(ascii_letters + digits, k=6))

            meta.alias = alias
            info_dict = meta.__dict__.copy()
            await session.commit()
            info_dict.pop('_sa_instance_state')
            return info_dict


async def stats_url(url: str = None, alias: str = None):
    if alias:
        meta = await get_link(alias=alias)
    else:
        meta = await get_link(url=url)
    if meta:
        info_dict = meta.__dict__.copy()
        info_dict.pop('_sa_instance_state')
        return info_dict
