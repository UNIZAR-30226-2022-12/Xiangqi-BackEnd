import code
from enum import Enum, IntEnum
from lib2to3.pytree import NegatedPattern
from unicodedata import name
from pydantic import BaseModel
import datetime

class Pais(IntEnum):
    name = 0
    code = 1 
    flag = 2 
    
class Skins(IntEnum):
    skinId = 0
    tipo = 1
    precio = 2

class Tiene(IntEnum):
    skinId = 0
    usuario = 1

class Chat(IntEnum):
    chatId = 0
    partidaId = 1
    jugadorRoja = 2
    jugadorNegra = 3
    
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
    
class Skins(IntEnum):
    skinId = 0
    tipo = 1 
    name = 2 
    description = 3 
    category = 4 
    precio = 5  

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
    date: datetime.datetime
    country: Country
    pwd: str
    image: bytes
    
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

class IdPartida(BaseModel):
    id: int
    
class Id(BaseModel):
    id: int

class Nickname(BaseModel):
    nickname: str
    
class PurchaseData(BaseModel):
    id: str
    tipo: str
    price: str