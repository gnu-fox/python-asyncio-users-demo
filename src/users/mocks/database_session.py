import uuid
from typing import Set

from src.users.auth.models.credentials import Credential
from src.users.auth.models.security import Security

TEST_CREDENTIALS = [Credential(
    id=uuid.uuid4(), 
    username="admin", 
    email="admin@gmail.com", 
    password=Security.hash("admin")
)]

class Session:
    _credentials : Set[Credential] = set(TEST_CREDENTIALS)

    @classmethod
    def _update(cls, credentials : Set[Credential]):
        cls._credentials.update(credentials)

    def __init__(self):
        self.credentials : Set[Credential] = None

    async def begin(self):
        self.credentials = self._credentials.copy()

    async def commit(self):
        self._update(self.credentials)

    async def rollback(self):
        self.credentials.clear()

    async def close(self):
        self.credentials.clear()