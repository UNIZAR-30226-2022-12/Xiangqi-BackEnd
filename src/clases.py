import code
from enum import IntEnum
from lib2to3.pytree import NegatedPattern
from unicodedata import name
from pydantic import BaseModel
import datetime

class Usuarios(IntEnum):
    id = 0
    correo = 1
    pwd = 2
    salt = 3 
    validacion = 4 
    nick = 5
    name = 6 
    birthDate = 7 
    pais = 8
    fichaSkin = 9
    tableroSkin = 10 
    rango = 11
    puntos = 12 
    fechaRegistro = 13

class Partidas(IntEnum):
    id = 0
    roja = 1 
    negra = 2 
    estado = 3 
    movimientos = 4 
    fechaInicio = 5 
    lastMove = 6 

class Pais(IntEnum):
    name = 0
    code = 1 
    flag = 2 

class Country(BaseModel):
    code: str
    name: str

class User(BaseModel):
    nickname: str
    name: str
    email: str
    image: bytes
    date: datetime.date
    country: Country
    pwd: str

class UpdateUser(BaseModel):
    nickname: str
    name: str
    image: bytes
    date: datetime.datetime
    country: Country
    pwd: str

class LoginData(BaseModel):
    email: str
    pwd: str

class EmailData(BaseModel):
    email: str


class Image(BaseModel):
    image: bytes