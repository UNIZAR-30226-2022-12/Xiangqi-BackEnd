from pydantic import BaseModel
import datetime

class Country(BaseModel):
    code: str
    name: str

class User(BaseModel):
    nickname: str
    name: str
    email: str
    date: datetime.datetime
    country: Country
    pwd: str

class LoginData(BaseModel):
    email: str
    pwd: str

class EmailData(BaseModel):
    email: str