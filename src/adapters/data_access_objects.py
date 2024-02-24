from typing import Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import Credential
from src.users.ports import Credentials
from src.adapters.database_schemas import Accounts

class SQLAlchemyCredentials(Credentials):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, credential : Credential):
        command = insert(Accounts).values(credential.model_dump(exclude_none=True))
        await self.session.execute(command)

    async def read(self, **kwargs) -> Optional[Credential]:
        query = select(Accounts).where(**kwargs)
        result = await self.session.execute(query)
        account = result.scalars().first()
        if account:
            return Credential(id=account.id, username=account.username, password=account.password)

    async def update(self, credential : Credential):
        command = update(Accounts).where(Accounts.id == credential.id).values(credential.model_dump(exclude_none=True))
        await self.session.execute(command)

    async def delete(self, credential : Credential):
        command = delete(Accounts).where(Accounts.id == credential.id)
        await self.session.execute(command)