from typing import Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import Credential
from src.users.ports import Credentials
from src.adapters.database_schemas import AccountSchema

class SQLAlchemyCredentials(Credentials):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, credential : Credential):
        command = insert(AccountSchema).values(credential.model_dump(exclude_none=True))
        await self.session.execute(command)

    async def read(self, **kwargs) -> Optional[Credential]:
        query = select(AccountSchema).filter_by(**kwargs)
        result = await self.session.execute(query)
        account = result.scalars().first()
        if account:
            return Credential(id=account.id, username=account.username, password=account.password)

    async def update(self, credential : Credential):
        command = update(AccountSchema).where(AccountSchema.id == credential.id).values(
            credential.model_dump(exclude='id', exclude_none=True)
        )
        await self.session.execute(command)

    async def delete(self, credential : Credential):
        if credential.id:
            command = delete(AccountSchema).where(AccountSchema.id == credential.id)
        elif credential.username:
            command = delete(AccountSchema).where(AccountSchema.username == credential.username)
        else:
            raise ValueError('No valid criteria to delete account')
        await self.session.execute(command)