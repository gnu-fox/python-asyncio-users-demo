from abc import ABC, abstractmethod
from typing import Set
from typing import Generator
from typing import Protocol
from typing import TypeVar, Generic
from typing import Deque

from src.users.models import Event

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