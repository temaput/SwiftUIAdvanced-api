
from pydantic import BaseModel


class User(BaseModel):
    username: str
    disabled: bool = False


class SignupDTO(BaseModel):
    username: str
    password: str



class UserInDB(BaseModel):
    username: str
    disabled: bool = False
    hashed_password: str = ""



class TokenDTO(BaseModel):
    access_token: str
    token_type: str