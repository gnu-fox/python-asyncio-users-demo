from uuid import UUID

from pydantic import Field
from datetime import timedelta
from pydantic.dataclasses import dataclass

from src.users.auth.models.credentials import Credential
from src.users.auth.models.tokens import Token, Claim
from src.users.auth.models.tokens import Tokenizer

@dataclass
class Account:
    id : UUID = Field(..., alias='id', description="The UUID of the Account")

    def create_token(self, timedelta : timedelta = timedelta(minutes=15)) -> Token:
        claim = Claim(sub=self.id, exp=timedelta)
        return Tokenizer.encode(claim)