import code
from enum import IntEnum
from lib2to3.pytree import NegatedPattern
from unicodedata import name
from pydantic import BaseModel
import datetime

class Usuarios(IntEnum):
    correo = 0
    pwd = 1 
    salt = 2 
    validacion = 3 
    nick = 4 
    name = 5 
    birthDate = 6 
    pais = 7 
    fichaSkin = 8
    tableroSkin = 9 
    rango = 10 
    puntos = 11 
    fechaRegistro = 12

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
    bandera = 2 

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