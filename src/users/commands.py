from typing import Optional
from uuid import UUID
from pydantic import SecretStr
from pydantic import EmailStr

from src.users.ports import Command

class StartApplication(Command):
    pass

class CreateAccount(Command):
    id : Optional[UUID] = None
    username : Optional[str] = None
    password : Optional[SecretStr] = None
    email : Optional[EmailStr] = None