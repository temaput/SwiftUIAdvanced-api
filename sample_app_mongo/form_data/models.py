from typing import Annotated
from fastapi import File
from pydantic import BaseModel, Field

class PlainForm(BaseModel):
      
  username: str
  password: str
  rank: int
  active: bool


class PlainFormWithFile(PlainForm):
    avatar: Annotated[bytes, File()]
