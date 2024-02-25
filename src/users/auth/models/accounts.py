from uuid import UUID
from datetime import timedelta
from typing import Deque
from collections import deque

from pydantic import Field
from pydantic.dataclasses import dataclass

from src.users.ports import Event
from src.users.auth.models.credentials import Credential
from src.users.auth.models.tokens import Token, Claim
from src.users.auth.models.tokens import Tokenizer

@dataclass
class Account:
    id : UUID = Field(..., alias='id', description="The UUID of the Account")
    events : Deque[Event] = deque()
    saved : bool = False

    def create_token(self, timedelta : timedelta = timedelta(minutes=15)) -> Token:
        claim = Claim(sub=self.id, exp=timedelta)
        return Tokenizer.encode(claim)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return self.id == __value.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)