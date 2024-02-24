from typing import Any
from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.data_access_objects import SQLAlchemyCredentials

class SessionFactory:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()    


class SQLAlchemyAccounts:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def commit(self):
        await self.session.commit()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = SQLAlchemyCredentials(session=self.session)
        await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()