import json
import pyodbc
import logging
import azure.functions as func
import bcrypt



def connectToDatabase():
    server = 'tradingapplicationserver.database.windows.net'
    database = 'TradingIndicatorDB'
    username = 'mvgachev'
    password = 'Katrin10'
    driver= '{ODBC Driver 17 for SQL Server}'

    connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    return cursor



def getUserWithEmail(email: str):
    cursor = connectToDatabase()
    cursor.execute('SELECT * FROM Users WHERE email = ?', email)
    user = cursor.fetchone()
    return user

def checkIfEmailExists(email: str):
    user = getUserWithEmail(email)
    if user is None:
        return False
    else:
        return True

def registerUser(email: str, discordUsername:str, password:str):
    cursor = connectToDatabase()
    cursor.execute('INSERT INTO Users (email, discord_username) VALUES(?,?)'
    , (email, discordUsername))
    cursor.connection.commit()
    if cursor.rowcount != 1:
        response = {
            "success": "false",
            "msg": "Something went wrong with the registration request. Please try again!"
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )  
    
    userId = getUserId(email)
    logging.info('Last user id was ' + str(userId))
    hashedPassword = encryptPassword(password)
    cursor.execute('INSERT INTO Passwords (user_id, password) VALUES(?,?)', (userId, hashedPassword))
    cursor.connection.commit()

    if cursor.rowcount == 1:
        response = {
            "success": "true",
            "msg": "You have registered successfully",
            "user": {
                "id": userId,
                "email": email,
                "discord_username": discordUsername
            }
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Something was wrong with the registration request. Please try again!",
            status_code=400
        )      


def getUserId(email):
    user = getUserWithEmail(email)
    userId = user[0]
    return userId

def encryptPassword(password:str):
    encodedPassword = password.encode("ascii")
    hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
    return hashedPassword