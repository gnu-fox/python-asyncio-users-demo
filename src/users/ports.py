from abc import ABC, abstractmethod
from typing import Set
from typing import Generator
from typing import Protocol
from typing import TypeVar, Generic
from typing import Any
from typing import Deque
from typing import Optional

from src.users.models import Event
from src.users.auth.models.credentials import Credential

class Aggregate(Protocol):
    id : str
    saved : bool
    events : Deque[Event]

T = TypeVar('T', bound=Aggregate)
class Repository(Generic[T]):
    def __init__(self, collection : Set[T] = set()):
        self.collection = collection

    def collect_events(self) -> Generator[Event, None, None]:
        for aggregate in self.collection:
            if aggregate.saved:
                while aggregate.events:
                    yield aggregate.events.popleft()
            aggregate.saved = False

    def add(self, aggregate : T):
        self.collection.add(aggregate)

    def get(self, id) -> T:
        for aggregate in self.collection:
            if aggregate.id == id:
                return aggregate
        return None
    
    def remove(self, aggregate : T):
        self.collection.remove(aggregate)
        

T = TypeVar('T')
class Factory(ABC, Generic[T]):

    @abstractmethod
    def __call__(self) -> T:
        pass


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

class UnitOfWork(ABC):
    
    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        ...

    @abstractmethod
    async def commit(self):
        ...
        

class Accounts(UnitOfWork):

    def __init__(self):
        self.credentials : Credentials