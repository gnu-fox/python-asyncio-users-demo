from uuid import uuid4
from uuid import UUID
from datetime import datetime
from typing import Deque
from collections import deque

from pydantic import BaseModel
from pydantic import Field

from src.users.ports import Event
from src.users.auth.models.accounts import Account
from src.users.auth.models.credentials import Credential

class User:
    def __init__(self, account : Account):
        self.account = account

    def save(self):
        self.account.saved = True

    @property
    def id(self) -> UUID:
        return self.account.id