import pytest
import uuid
import logging
from typing import Generator

from src.adapters.mock.sessions import Session
from src.adapters.mock.units_of_work import MockAccounts

from src.users.auth.models.credentials import Credential
from src.users.auth.models.security import Security
from src.users.auth.ports import Accounts
from src.users.auth import services
from src.users.auth import exceptions

LOGGER = logging.getLogger(__name__)

@pytest.fixture
def accounts() -> Generator[Accounts, None, None]:
    yield MockAccounts()


@pytest.mark.asyncio
async def test_accounts(accounts : Accounts):
    async with accounts:
        credential = await accounts.credentials.read(username="admin")
        assert credential.username == "admin"


@pytest.mark.asyncio
async def test_register(accounts : Accounts):
    with pytest.raises(exceptions.AccountAlreadyExists):
        LOGGER.info("Testing Register on an already existing account")
        credential = Credential(username="admin", password="admin")
        await services.register(credential, accounts)

    with pytest.raises(exceptions.InvalidCredential):
        LOGGER.info("Testing Register with no password")
        credential = Credential(username="test")
        await services.register(credential, accounts)

    credential = Credential(username="test", password="test")
    await services.register(credential, accounts)

    async with accounts:
        retrieved = await accounts.credentials.read(username="test")
        assert retrieved.username == "test"
        assert Security.verify("test", retrieved.password) == True


@pytest.mark.asyncio
async def test_authenticate(accounts : Accounts):
    with pytest.raises(exceptions.AccountNotFound):
        LOGGER.info("Testing Authenticate with non-existing account")
        credential = Credential(username="non-existing")
        await services.authenticate(credential, accounts)

    with pytest.raises(exceptions.InvalidCredential):
        LOGGER.info("Testing Authenticate with wrong password")
        credential = Credential(username="admin", password="wrong")
        await services.authenticate(credential, accounts)

    credential = Credential(username="admin", password="admin")
    account = await services.authenticate(credential, accounts)
    assert account.id