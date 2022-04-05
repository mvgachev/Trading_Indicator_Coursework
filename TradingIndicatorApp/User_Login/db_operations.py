import pyodbc
import bcrypt

from User_Registration.db_operations import getUserWithEmail
from User_Registration.db_operations import connectToDatabase

def getPasswordOfUser(user):
    cursor = connectToDatabase()
    userId = user[0]
    cursor.execute('SELECT * FROM Passwords WHERE user_id = ?', userId)
    userAuth = cursor.fetchone()
    return userAuth[1]

def checkIfPasswordMatch(password: str, email: str):
    user = getUserWithEmail(email)
    providedPasswordEncoded = password.encode("ascii")
    userPasswordHashed = getPasswordOfUser(user)
    if bcrypt.checkpw(providedPasswordEncoded, userPasswordHashed):
        return True
    else:
        return False
