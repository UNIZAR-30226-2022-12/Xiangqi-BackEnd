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
    "  salt TINYTEXT NOT NULL,"
    "  validado BOOLEAN,"
    "  nick VARCHAR(20) NOT NULL,"
    "  name VARCHAR(100) NOT NULL,"
    "  birthDate VARCHAR(100) NOT NULL,"
    "  pais VARCHAR(50) NOT NULL,"
    "  fichaSkin INT,"
    "  tableroSkin INT,"
    "  rango INT,"
    "  puntos INT,"
    "  fechaRegistro VARCHAR(100),"
    "  PRIMARY KEY (correo),"
    "  FOREIGN KEY (fichaSkin) REFERENCES Skins(skinId)"
    "  ON DELETE SET NULL,"
    "  FOREIGN KEY (tableroSkin) REFERENCES Skins(skinId)"
    "  ON DELETE SET NULL"
    "  "
    ");")

TABLES['Amigos'] = (
    "CREATE TABLE Amigos ("
    "  usuario1 VARCHAR(100) NOT NULL,"
    "  usuario2 VARCHAR(100) NOT NULL,"
    "  FOREIGN KEY (usuario1) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (usuario2) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
    ");")

TABLES['Tiene'] = (
    "CREATE TABLE Tiene ("
    "  skinId INT NOT NULL,"
    "  usuario VARCHAR(100) NOT NULL,"
    "  FOREIGN KEY (usuario) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (skinId) REFERENCES Skins(skinId)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
    ");")

TABLES['Partidas'] = (
    "CREATE TABLE Partidas ("
    "  id INT NOT NULL AUTO_INCREMENT,"
    "  roja VARCHAR(100) NOT NULL,"
    "  negra VARCHAR(100) NOT NULL,"
    "  estado INT NOT NULL," #0 en curso, 1 gana rojo, 2 gana negra, 3 empate 
    "  movimientos LONGTEXT," 
    "  fechaInicio VARCHAR(100),"
    "  lastMove VARCHAR(100),"
    "  PRIMARY KEY (id),"
    "  FOREIGN KEY (roja) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (negra) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
    ");")

TABLES['Solicitudes'] = (
    "CREATE TABLE Solicitudes ("
    "  remitente VARCHAR(100) NOT NULL,"
    "  destinatario VARCHAR(100) NOT NULL,"
    "  FOREIGN KEY (remitente) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (destinatario) REFERENCES Usuarios(correo)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
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
