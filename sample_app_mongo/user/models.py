from bson import ObjectId
from pydantic import BaseModel, Field

from ..database import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    username: str
    disabled: bool = False

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}
    


class SignupDTO(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str
    
   

class TokenDTO(BaseModel):
    access_token: str
    token_type: str