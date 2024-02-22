from typing import Union
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import field_serializer, field_validator

from src.users.auth.models.security import Security

class Credential(BaseModel):
    id : UUID = Field(default=None, alias="id", description="The UUID of the Account")
    username : str = Field(default=None, alias="username", description="The username of the Account")
    password : SecretStr = Field(default=None, alias="password", description="The password of the Account")
    email : EmailStr = Field(default=None, alias="email", description="The email of the Account")

    @field_serializer('password', when_used='always')
    def reveal(password : SecretStr) -> str:
        return password.get_secret_value()
    
    def hash_secrets(self):
        self.password = Security.hash(self.password)

    def verify_password(self, password : Union[str, SecretStr]) -> bool:
        return Security.verify(password, self.password)
    
credentials = Credential(username="username", password="password")
credentials.id = UUID("00000000-0000-0000-0000-000000000000")

print(credentials)
