from src.users.mocks.database_session import Session
from src.users.mocks.data_access_objects import MockCredentials

class MockAccounts:

    async def __aenter__(self):
        self.session = Session()
        self.credentials = MockCredentials(self.session)
        await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.commit()

    async def commit(self):
        await self.session.commit()