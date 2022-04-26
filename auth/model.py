from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class User(BaseModel):
    username: str = Query("", min_length=4, max_length=16, regex="^[a-zA-Z0-9]{4,16}$")
    password: str = Query("", min_length=8, regex="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")
    email: str = Query("", min_length=8, regex="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,6}$")
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None
