from uuid import uuid4
from uuid import UUID
from datetime import datetime
from typing import Deque
from collections import deque

from pydantic import BaseModel
from pydantic import Field

from src.users.auth.models.accounts import Account
from src.users.auth.models.credentials import Credential

class Metadata(BaseModel):
    type : str = Field(description="The type of message.")
    id : UUID = Field(default_factory=uuid4, description="The unique identifier for the message.")
    timestamp : datetime = Field(default_factory=datetime.now, description="The time the message was created.")

class Event(BaseModel):
    metadata : Metadata = Metadata(type="event")

class Command(BaseModel):
    metadata : Metadata = Metadata(type="command")

class User:
    def __init__(self, account : Account):
        self.account = account
        self.events : Deque[Event] = deque()
        self.saved = False

    def save(self):
        self.saved = True

    @property
    def id(self):
        return self.account.id
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return self.id == __value.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)