from uuid import UUID
from datetime import timedelta

from src.users.auth.models.accounts import Account
from src.users.auth.models.tokens import Token, Claim
from src.users.auth.models.tokens import Tokenizer

class User:
    def __init__(self, account : Account):
        self.account = account

    def save(self):
        self.account.saved = True

    @property
    def id(self) -> UUID:
        return self.account.id

    def create_token(self, timedelta : timedelta = timedelta(minutes=15)) -> Token:
        claim = Claim(sub=self.id, exp=timedelta)
        return Tokenizer.encode(claim)
