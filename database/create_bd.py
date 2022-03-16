import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

cursor = cnx.cursor()

TABLES = {} #Añadir tablas aqui
TABLES['Skins'] = (
    "CREATE TABLE Skins ("
    "  skinId INT NOT NULL AUTO_INCREMENT,"
    "  tipo BOOL NOT NULL," # 0 skin de ficha, 1 skin de tablero
    "  precio INT,"
    "  PRIMARY KEY (skinId)"
    ");")

TABLES['Usuarios'] = (
    "CREATE TABLE Usuarios ("
    "  correo VARCHAR(100) NOT NULL,"
    "  pwd TINYTEXT NOT NULL,"
    "  nick VARCHAR(20) NOT NULL,"
    "  name VARCHAR(100) NOT NULL,"
    "  birthDate DATE NOT NULL,"
    "  foto TINYTEXT NOT NULL,"
    "  pais VARCHAR(50) NOT NULL,"
    "  fichaSkin INT,"
    "  tableroSkin INT,"
    "  rango INT,"
    "  puntos INT,"
    "  fechaRegistro DATE,"
    "  PRIMARY KEY (correo),"
    "  FOREIGN KEY (fichaSkin) REFERENCES Skins(skinId),"
    "  FOREIGN KEY (tableroSkin) REFERENCES Skins(skinId)"
    ");")

TABLES['Amigos'] = (
    "CREATE TABLE Amigos ("
    "  usuario1 VARCHAR(100) NOT NULL,"
    "  usuario2 VARCHAR(100) NOT NULL,"
    "  FOREIGN KEY (usuario1) REFERENCES Usuarios(correo),"
    "  FOREIGN KEY (usuario2) REFERENCES Usuarios(correo)"
    ");")

TABLES['Tiene'] = (
    "CREATE TABLE Tiene ("
    "  skinId INT NOT NULL,"
    "  usuario VARCHAR(100) NOT NULL,"
    "  FOREIGN KEY (usuario) REFERENCES Usuarios(correo),"
    "  FOREIGN KEY (skinId) REFERENCES Skins(skinId)"
    ");")

TABLES['Partidas'] = (
    "CREATE TABLE Partidas ("
    "  id INT NOT NULL AUTO_INCREMENT,"
    "  roja VARCHAR(100) NOT NULL,"
    "  negra VARCHAR(100) NOT NULL,"
    "  estado INT NOT NULL," #0 en curso, 1 gana rojo, 2 gana negra, 3 empate 
    "  movimientos LONGTEXT,"
    "  fechaInicio DATE,"
    "  lastMove DATE,"
    "  PRIMARY KEY (id),"
    "  FOREIGN KEY (roja) REFERENCES Usuarios(correo),"
    "  FOREIGN KEY (negra) REFERENCES Usuarios(correo)"
    ");")

TABLES['Solicitudes'] = (
    "CREATE TABLE Solicitudes ("
    "  remitente VARCHAR(100) NOT NULL,"
    "  destinatario VARCHAR(100) NOT NULL,"
    "  FOREIGN KEY (remitente) REFERENCES Usuarios(correo),"
    "  FOREIGN KEY (destinatario) REFERENCES Usuarios(correo)"
    ");")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
