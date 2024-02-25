import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from typing import Dict
from typing import Callable
from typing import List
from typing import Union
from collections import deque

from src.users.auth.ports import Accounts
from src.users.settings import Settings
from src.users.models import User, Account
from src.users.ports import Event, Command
from src.users.ports import Repository
from src.users import events
from src.users import commands
from src.users import handlers

class Application:
    def __init__(self, repository : Repository):
        self.repository = repository
        self.publishers : Dict[Event, Callable[[Command], None]] = {}
        self.consumers : Dict[Event, List[Callable[[Event], None]]] = {}
        self.queue = deque()

    async def handle(self, message : Union[Event, Command]):
        self.queue.append(message)
        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Command):
                await self.publish(message)
            elif isinstance(message, Event):
                await self.consume(message)

    async def publish(self, command: Command):
        try:
            await self.publishers[type(command)](command)
            self.queue.extend(self.repository.collect_events())
        except Exception:
            raise
    
    async def consume(self, event: Event):
        for handler in self.consumers[type(event)]:
            try:
                await handler(event)
                self.queue.extend(self.repository.collect_events())
            except Exception:
                continue

T = TypeVar('T')
class Factory(ABC, Generic[T]):

    @abstractmethod
    def create(self) -> T:
        pass


def create_accounts_uow(settings : Settings) -> Accounts:
    return settings.accounts_backend(**settings.accounts_backend_args)

class Users:
    repository : Repository[Account] = Repository(collection=set())

    def __init__(self, settings : Settings):
        self.settings = settings
        self.collection = self.repository.collection
        self.application : Application = Application(repository=self.repository)
        self.application.publishers[commands.StartApplication] = handlers.Start()
        self.application.consumers[events.UserCreated] = [handlers.CreateAccount(accounts=create_accounts_uow(settings))]

    async def __aenter__(self):
        self.accounts = create_accounts_uow(self.settings)
        await self.accounts.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        self.application.queue.extend(self.repository.collect_events())
        await self.application.handle(commands.StartApplication())
        await self.accounts.__aexit__(exc_type, exc_value, traceback)

    async def create(self, **kwargs) -> User:
        account = Account(id = uuid.uuid4())
        account.events.append(events.UserCreated(**kwargs))
        self.collection.add(account)
        return User(account=account)
    
    async def read(self, **kwargs) -> User:
        async with self.accounts:
            credential = await self.accounts.credentials.read(**kwargs)
            if credential:
                account = Account(id = credential.id)
                self.collection.add(account)
                return User(account=account)