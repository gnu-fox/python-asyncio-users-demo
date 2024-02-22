import uuid
from typing import Set
from src.users.auth.models.credentials import Credential

class Session:
    existing = Credential(id=uuid.uuid4(), username="admin", email="admin@gmail.com", password="password").hash()

    _credentials : Set[Credential] = set()
    _credentials.add(existing)

    def __init__(self):
        self.credentials : Set[Credential] = self._credentials.copy()
        for credential in self.credentials:
            print(credential)

    async def begin(self):
        pass

    @classmethod
    async def commit(self):
        self._credentials.update(self.credentials)

    async def rollback(self):
        self.credentials.clear()

    async def close(self):
        self.credentials.clear()
        
async def main():
    session = Session()
    print(session.credentials)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())