from abc import ABC, abstractmethod
from typing import Protocol
from typing import Optional
from typing import Any

from src.users.auth.models.credentials import Credential

class Credentials(ABC):

    @abstractmethod
    async def create(self, credential : Credential):
        ...

    @abstractmethod
    async def read(self, **kwargs) -> Optional[Credential]: 
        ...

    @abstractmethod
    async def update(self, credential : Credential):
        ...

    @abstractmethod
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