from typing import Optional
from uuid import UUID
from pydantic import SecretStr
from pydantic import EmailStr

from src.users.models import Command

class StartApplication(Command):
    pass