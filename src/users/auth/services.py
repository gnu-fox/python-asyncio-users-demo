from src.users.auth.models.accounts import Account
from src.users.auth.models.credentials import Credential
from src.users.auth.ports import Accounts
from src.users.auth import exceptions

async def authenticate(credential : Credential, accounts : Accounts) -> Account:
    async with accounts:
        if credential.username:
            retrieved = await accounts.credentials.read(username=credential.username)
        elif credential.email:
            retrieved = await accounts.credentials.read(email=credential.email)
        else:
            raise exceptions.InvalidCredential

    if not retrieved:
        raise exceptions.AccountNotFound
    
    if credential.password:
        if not retrieved.verify_password(credential.password):
            raise exceptions.InvalidCredential

    return Account(id=retrieved.id)
    

async def register(credential : Credential, accounts : Accounts):
    async with accounts:
        if credential.username:
            retrieved = await accounts.credentials.read(username=credential.username)
        elif credential.email:
            retrieved = await accounts.credentials.read(email=credential.email)
        else:
            raise exceptions.InvalidCredential
        
    if retrieved:
        raise exceptions.AccountAlreadyExists
    
    if credential.password:
        credential.hash_password()   
    else:
        raise exceptions.InvalidCredential

    if not credential.id:
        credential.generate_id()
 
    async with accounts:
        await accounts.credentials.create(credential)
        await accounts.commit()