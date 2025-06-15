from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: Optional[str] = None
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
