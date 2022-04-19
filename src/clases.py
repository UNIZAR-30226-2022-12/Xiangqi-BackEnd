import code
from enum import Enum, IntEnum
from lib2to3.pytree import NegatedPattern
from unicodedata import name
from pydantic import BaseModel
import datetime

class P(Enum):
    hh = 0 #hueco
    pr = 1 #peon rojo
    kr = 2 #cañon rojo
    tr = 3 #torreo rojo
    cr = 4 #caballo rojo
    ar = 5 #alfil rojo
    gr = 6 #general rojo
    rr = 7 #rey rojo
    pn = -1 #peon rojo
    kn = -2 #cañon rojo
    tn = -3 #torreo rojo
    cn = -4 #caballo rojo
    an = -5 #alfil rojo
    gn = -6 #general rojo
    rn = -7 #rey rojo

TABLERO = [[P.tn, P.cn, P.an, P.gn, P.rn, P.gn, P.an, P.cn, P.tn],
           [P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh],
           [P.hh, P.kn, P.hh, P.hh, P.hh, P.hh, P.hh, P.kn, P.hh],
           [P.pn, P.hh, P.pn, P.hh, P.pn, P.hh, P.pn, P.hh, P.pn],
           [P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh],
           [P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh],
           [P.pr, P.hh, P.pr, P.hh, P.pr, P.hh, P.pr, P.hh, P.pr],
           [P.hh, P.kr, P.hh, P.hh, P.hh, P.hh, P.hh, P.kr, P.hh],
           [P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh, P.hh],
           [P.tr, P.cr, P.ar, P.gr, P.rr, P.gr, P.ar, P.cr, P.tr]
           ]

class Pais(IntEnum):
    name = 0
    code = 1 
    flag = 2 
    
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
    
class Piezas(IntEnum):
    hh = 0
    pr1 = 1
    pr2 = 2
    pr3 = 3
    pr4 = 4
    kr1 = 5
    kr2 = 6
    tr1 = 7
    tr2 = 8
    cr1 = 9 
    cr2 = 10 
    ar1 = 11
    ar2 = 12
    gr1 = 13
    gr2 = 14
    rr = 15
    pn1 = -1
    pn2 = -2
    pn3 = -3
    pn4 = -4
    kn1 = -5
    kn2 = -6
    tn1 = -7
    tn2 = -8
    cn1 = -9 
    cn2 = -10 
    an1 = -11
    an2 = -12
    gn1 = -13
    gn2 = -14
    rn = -15 

class equipoRojo(IntEnum):
    pr1 = 1
    pr2 = 2
    pr3 = 3
    pr4 = 4
    kr1 = 5
    kr2 = 6
    tr1 = 7
    tr2 = 8
    cr1 = 9 
    cr2 = 10 
    ar1 = 11
    ar2 = 12
    gr1 = 13
    gr2 = 14
    rr = 15
    
class equipoNegro(IntEnum):
    pn1 = -1
    pn2 = -2
    pn3 = -3
    pn4 = -4
    kn1 = -5
    kn2 = -6
    tn1 = -7
    tn2 = -8
    cn1 = -9 
    cn2 = -10 
    an1 = -11
    an2 = -12
    gn1 = -13
    gn2 = -14
    rn = -15    
    
class Skins(IntEnum):
    skinId = 0
    tipo = 1
    precio = 2

class Tiene(IntEnum):
    skinId = 0
    usuario = 1
    

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

class SkinShop(BaseModel):
    image: bytes
    kindOf: int
    price: int
    
class SkinUser(BaseModel):
    image: bytes
    kindOf: int

class Image(BaseModel):
    image: bytes