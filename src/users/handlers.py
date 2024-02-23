from typing import TypeVar, Generic
from typing import Union
from abc import ABC, abstractmethod

from src.users.models import Event, Command
from src.users.auth.models.credentials import Credential
from src.users.auth.ports import Accounts
from src.users.auth import services as auth
from src.users import events, commands


T = TypeVar('T', bound=Union[Event, Command])
class Handler(ABC, Generic[T]):

    @abstractmethod
    async def __call__(self, message : T):
        pass


class CreateAccount(Handler[events.UserCreated]):
    def __init__(self, accounts : Accounts):
        self.accounts = accounts

    async def __call__(self, event : events.UserCreated):
        credential = Credential(**event.model_dump())
        await auth.register(credential=credential, accounts=self.accounts)


class Start(Handler[commands.StartApplication]):
    async def __call__(self, command : commands.StartApplication):
        pass