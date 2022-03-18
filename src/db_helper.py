#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
import mysql.connector

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

getUserQuery = "SELECT * FROM Usuarios WHERE correo = %s"
getAllUserQuery = "SELECT * FROM Usuarios"
getUserGameQuery = "SELECT * FROM Partidas WHERE roja = %s OR negra = %s"
insertUserQuery =  ("INSERT INTO Usuarios (correo, pwd, nick, name, birthDate, foto, pais, fichaSkin, tableroSkin, rango, puntos, fechaRegistro) "
        "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

def getAllUser():              
    cursor = cnx.cursor()
    cursor.execute(getAllUserQuery)

    userList = cursor.fetchall()
    
    cursor.close()

    return userList

def getUser(correo):
    exist = False

    cursor = cnx.cursor()

    cursor.execute(getUserQuery, (correo,))
    user = cursor.fetchone()

    if user != None :
        exist = True

    cursor.close()

    return exist, user

def getUserGame(correo):

    cursor = cnx.cursor()

    cursor.execute(getUserGameQuery, (correo, correo))
    game = cursor.fetchall()

    cursor.close()

    return game

def insertUser(user):
    try:
        cursor = cnx.cursor()
        exito = True

        cursor.execute(insertUserQuery, user)
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to insert record into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito



#cnx.close()