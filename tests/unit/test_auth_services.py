import uuid
import pytest
import asyncio
import logging

from src.users.auth.ports import Credentials
from src.users.auth.ports import Accounts
from src.users.auth.models.credentials import Credential
from src.users.auth.models.accounts import Account
from src.users.auth import exceptions
from src.users.auth import services


LOGGER = logging.getLogger(__name__)

@pytest.fixture
def accounts() -> Accounts:
    ...

@pytest.mark.asyncio
async def test_register(accounts : Accounts):
    LOGGER.info("Testing register")
    credential = Credential(username="admin", password="password")
    async with accounts:
        with pytest.raises(exceptions.AccountAlreadyExists):
            LOGGER.info("Testing account already exists")
            await services.register(credential, accounts)

    