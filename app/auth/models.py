from pydantic import BaseModel

class AuthItem(BaseModel):
    auth_token:str
