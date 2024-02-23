import pytest

from src.users.models import User
from src.users.application import Users


@pytest.mark.asyncio
async def test_users():
    async with Users() as users:
        user = await users.create(username = 'test', password = 'test')
        user.save()

    async with Users() as users:
        user = await users.read(username = 'test')
        assert user