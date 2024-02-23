from abc import ABC, abstractmethod
from typing import Protocol
from typing import Optional
from typing import Any

from src.users.auth.models.credentials import Credential

class Credentials(Protocol):

    async def create(self, credential : Credential):
        ...

    async def read(self, **kwargs) -> Optional[Credential]: 
        ...

    async def update(self, credential : Credential):
        ...

    async def delete(self, credential : Credential):
        ...


class Accounts(Protocol):
    credentials : Credentials

    async def commit(self):
        ...

    async def __aenter__(self):
        ...
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        ...