import pytest
import logging

from src.users.settings import Settings
from src.users.auth import exceptions
from src.users.models import User
from src.users.application import Users

LOGGER = logging.getLogger(__name__)

@pytest.fixture
def settings():
    return Settings(test=True)

@pytest.mark.asyncio
async def test_users(settings : Settings):

    LOGGER.info('Testing users')
    async with Users(settings=settings) as users:
        user = await users.create(username = 'test', password = 'test')
        user.save()

    user_id = user.id
    LOGGER.info(f'Created user with id: {user_id}')

    users = Users(settings=settings)
    async with users:
        user = await users.read(username = 'test')
        LOGGER.info(f'Retrieved user with id: {user.id} of type: {type(user.id)}')
        assert user

    async with users:
        user = await users.read(id = user.id)
        assert user

    async with users:
        user = await users.read(username = 'test22')
        assert not user