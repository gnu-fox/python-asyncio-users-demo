from src.adapters.mock.sessions import Session
from src.users.auth.models.credentials import Credential
from src.users.auth.ports import Credentials

class MockCredentials:
    def __init__(self, session : Session):
        self.session = session

    async def create(self, credential : Credential):
        self.session.credentials.add(credential)

    async def read(self, **kwargs):
        for credential in self.session.credentials:
            if all(getattr(credential, key) == value for key, value in kwargs.items()):
                return credential
        return None

    async def update(self, credential : Credential):
        self.session.credentials.remove(credential)
        self.session.credentials.add(credential)

    async def delete(self, credential : Credential):
        self.session.credentials.remove(credential)