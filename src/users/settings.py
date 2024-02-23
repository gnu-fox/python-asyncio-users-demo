from typing import Type
from typing import Dict
from typing import Union

from pydantic import ConfigDict
from pydantic import Field
from pydantic import computed_field
from pydantic import model_validator
from pydantic_settings import BaseSettings

from src.users.ports import Accounts
from src.users.mocks.units_of_work import MockAccounts

class Settings(BaseSettings):
    test : bool = False
    database_uri: Union[str, None] = Field(None, description="The URI of the database.")
    accounts_backend: Type
    accounts_backend_args: Dict    

    @model_validator(mode='before')
    @classmethod
    def generate_backend(cls, values):
        if values['test']:
            values['accounts_backend'] = MockAccounts
            values['accounts_backend_args'] = {}
        elif values['database_uri']:
            raise NotImplementedError
        return values