import uuid
from typing import Type
from typing import Dict
from typing import Callable
from typing import List
from typing import Union
from collections import deque

from src.users.models import Event, Command
from src.users.models import User, Account
from src.users.repository import Repository
from src.users import events
from src.users import commands
from src.users import handlers

from src.users.auth.ports import Accounts

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


class Users:
    repository : Repository[User] = Repository(collection=set())
    def __init__(self):
        self.collection = self.repository.collection
        self.application : Application = Application(repository=self.repository)

    async def __aenter__(self):
        self.application.consumers[events.UserCreated] = [handlers.CreateAccount(accounts=...)]
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        self.application.queue.extend(self.repository.collect_events())
        await self.application.handle(commands.StartApplication())

    async def create(self, **kwargs) -> User:
        account = Account(id = uuid.uuid4())
        user = User(account=account)
        user.events.append(events.UserCreated(**kwargs))
        self.collection.add(user)
        return user