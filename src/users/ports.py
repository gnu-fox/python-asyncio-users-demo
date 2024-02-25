from abc import ABC, abstractmethod
from uuid import uuid4
from uuid import UUID
from datetime import datetime
from typing import Set
from typing import Generator
from typing import Protocol
from typing import TypeVar, Generic
from typing import Deque

from pydantic import BaseModel
from pydantic import Field

class Metadata(BaseModel):
    type : str = Field(description="The type of message.")
    id : UUID = Field(default_factory=uuid4, description="The unique identifier for the message.")
    timestamp : datetime = Field(default_factory=datetime.now, description="The time the message was created.")

class Event(BaseModel):
    metadata : Metadata = Metadata(type="event")

class Command(BaseModel):
    metadata : Metadata = Metadata(type="command")

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