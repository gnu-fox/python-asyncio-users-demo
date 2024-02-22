import uuid
import pytest
import asyncio
import logging

from src.users.auth.ports import Credentials
from src.users.auth.models.credentials import Credential
from src.users.auth.models.accounts import Account
from src.users.auth import exceptions
from src.users.auth import services

LOGGER = logging.getLogger(__name__)

class Mocked(Credentials):
    def __init__(self, session):
        self.fake_session = session
        self.data = [Credential(id=uuid.uuid4(), username="username", email="email@gmail.com", password="password")]

    async def create(self, credential : Credential):
        self.data.append(credential)

    async def read(self, **kwargs) -> Credential:
        return self.data[0]

    async def update(self, credential : Credential):
        pass

    async def delete(self, credential : Credential):
        pass

class Accounts:    
    async def commit(self):
        pass

    async def __aenter__(self):
        self.credentials = Mocked(session=None)

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass


@pytest.mark.asyncio
async def test_register():
    LOGGER.info("Testing register")
    credential = Credential(username="username", email="email@gmail.com", password="password")
    accounts = Accounts()
    async with accounts:
        with pytest.raises(exceptions.AccountAlreadyExists):
            LOGGER.info("Testing account already exists")
            await services.register(credential, accounts)
        
