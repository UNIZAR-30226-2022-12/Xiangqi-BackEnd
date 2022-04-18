import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

cursor = cnx.cursor()

TABLES = {} #Añadir tablas aqui
TABLES['Country'] = (
    "CREATE TABLE Country ("
    "  name VARCHAR(50) NOT NULL,"
    "  code VARCHAR(5) NOT NULL," # 0 skin de ficha, 1 skin de tablero
    "  bandera VARCHAR(20),"
    "  PRIMARY KEY (name)"
    ");")

TABLES['Skins'] = (
    "CREATE TABLE Skins ("
    "  skinId INT NOT NULL AUTO_INCREMENT,"
    "  tipo BOOL NOT NULL," # 0 skin de ficha, 1 skin de tablero
    "  precio INT,"
    "  PRIMARY KEY (skinId)"
    ");")

TABLES['Usuarios'] = (
    "CREATE TABLE Usuarios ("
    "  id INT NOT NULL AUTO_INCREMENT,"
    "  correo VARCHAR(100) NOT NULL UNIQUE,"
    "  pwd TINYTEXT NOT NULL,"
    "  salt TINYTEXT NOT NULL,"
    "  validacion BOOLEAN,"
    "  nick VARCHAR(20) NOT NULL,"
    "  name VARCHAR(100) NOT NULL,"
    "  birthDate DATE NOT NULL,"
    "  pais VARCHAR(20),"
    "  fichaSkin INT,"
    "  tableroSkin INT,"
    "  rango INT,"
    "  puntos INT,"
    "  fechaRegistro DATE,"
    "  PRIMARY KEY (id),"
    "  FOREIGN KEY (pais) REFERENCES Country(name)"
    "  ON DELETE SET NULL,"
    "  FOREIGN KEY (fichaSkin) REFERENCES Skins(skinId)"
    "  ON DELETE SET NULL,"
    "  FOREIGN KEY (tableroSkin) REFERENCES Skins(skinId)"
    "  ON DELETE SET NULL"
    ");")

TABLES['Amigos'] = (
    "CREATE TABLE Amigos ("
    "  usuario1 INT NOT NULL,"
    "  usuario2 INT NOT NULL,"
    "  FOREIGN KEY (usuario1) REFERENCES Usuarios(id)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (usuario2) REFERENCES Usuarios(id)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
    ");")

TABLES['Tiene'] = (
    "CREATE TABLE Tiene ("
    "  skinId INT NOT NULL,"
    "  usuario INT NOT NULL,"
    "  FOREIGN KEY (usuario) REFERENCES Usuarios(id)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (skinId) REFERENCES Skins(skinId)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
    ");")

TABLES['Partidas'] = (
    "CREATE TABLE Partidas ("
    "  id INT NOT NULL AUTO_INCREMENT,"
    "  roja INT NOT NULL,"
    "  negra INT,"
    "  estado INT NOT NULL," #-1 sin oponente, 0 en curso, 1 gana rojo, 2 gana negra, 3 empate 
    "  movimientos LONGTEXT," 
    "  fechaInicio DATETIME,"
    "  lastMove DATETIME,"
    "  PRIMARY KEY (id),"
    "  FOREIGN KEY (roja) REFERENCES Usuarios(id)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (negra) REFERENCES Usuarios(id)"
    "  ON DELETE CASCADE ON UPDATE CASCADE"
    ");")

TABLES['Solicitudes'] = (
    "CREATE TABLE Solicitudes ("
    "  remitente INT NOT NULL,"
    "  destinatario INT NOT NULL,"
    "  FOREIGN KEY (remitente) REFERENCES Usuarios(id)"
    "  ON DELETE CASCADE ON UPDATE CASCADE,"
    "  FOREIGN KEY (destinatario) REFERENCES Usuarios(id)"
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
