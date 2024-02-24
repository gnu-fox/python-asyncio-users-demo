import pytest
import socket
from uuid import uuid4

from sqlalchemy import URL
from sqlalchemy import select, insert, update, delete

from src.users.models import Credential
from src.adapters.database_schemas import AccountSchema
from src.adapters.data_access_objects import SQLAlchemyCredentials
from src.adapters.units_of_work import SessionFactory
from src.adapters.units_of_work import SQLAlchemyAccounts

@pytest.fixture
def url():
    return URL.create(
        drivername = 'postgresql+asyncpg',
        username = 'postgres',
        password = 'postgres',
        host = socket.gethostbyname('postgres'),
        port = 5432,
        database = 'postgres'
    )

@pytest.mark.asyncio
async def test_create_account(url : URL):
    uow = SQLAlchemyAccounts(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with uow:
        command = delete(AccountSchema).where(AccountSchema.username == 'test')
        await uow.accounts.session.execute(command)
        await uow.commit()

        try:
            await uow.accounts.create(credential=Credential(id = identity, username='test', password='test'))
            await uow.commit()
        except Exception:
            print('Account already in database. Skip')
            raise

    async with uow:
        try:
            query = select(AccountSchema).where(AccountSchema.username == 'test')
            result = await uow.accounts.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test'
        
        finally:
            command = delete(AccountSchema).where(AccountSchema.username == 'test')
            await uow.accounts.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_read_account(url : URL):
    uow = SQLAlchemyAccounts(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with uow:
        try:
            command = insert(AccountSchema).values(id=identity, username='test', password='test')
            await uow.accounts.session.execute(command)
            await uow.commit()        
        except Exception:
            print('Account already in database. Skip')
            pass
    
    async with uow:
        try:
            account = await uow.accounts.read(username='test')
            assert account.id == identity

        finally:
            command = delete(AccountSchema).where(AccountSchema.username == 'test')
            await uow.accounts.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_update_account(url : URL):
    uow = SQLAlchemyAccounts(session_factory=SessionFactory(url=url))
    identity = uuid4()

    async with uow:
        try:
            command = insert(AccountSchema).values(id=identity, username='test', password='test')
            await uow.accounts.session.execute(command)
            await uow.commit()        
        except Exception:
            print('Account already in database. Skip')
            pass
    
    try:
        async with uow:
            await uow.accounts.update(Credential(id=identity, username='test2'))
            await uow.commit()

        async with uow:
            query = select(AccountSchema).where(AccountSchema.id==identity)
            result = await uow.accounts.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test2'

    finally:
        async with uow:
            command = delete(AccountSchema).where(AccountSchema.id == identity)
            await uow.accounts.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_delete_account(url : URL):
    uow = SQLAlchemyAccounts(session_factory=SessionFactory(url=url))
    identity = uuid4()

    async with uow:
        try:
            command = insert(AccountSchema).values(id=identity, username='test', password='test')
            await uow.accounts.session.execute(command)
            await uow.commit()        
        except Exception:
            print('Account already in database. Skip')
            pass

    async with uow:
        query = select(AccountSchema).where(AccountSchema.username == 'test')
        result = await uow.accounts.session.execute(query)
        schema = result.scalars().first()
        assert schema.username == 'test'

    async with uow:
        await uow.accounts.delete(credential=Credential(id=identity))
        await uow.commit()

    async with uow:
        query = select(AccountSchema).where(AccountSchema.username == 'test')
        result = await uow.accounts.session.execute(query)
        schema = result.scalars().first()
        assert schema is None