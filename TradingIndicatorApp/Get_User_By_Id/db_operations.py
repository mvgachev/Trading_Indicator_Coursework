import json
import azure.functions as func

from User_Registration.db_operations import connectToDatabase



def getUserWithId(userId: int):
    cursor = connectToDatabase()
    cursor.execute('SELECT * FROM Users WHERE id = ?', userId)

    user = cursor.fetchone()
    response = {
        "success": "true",
        "user": {
            "id": user.id,
            "email": user.email,
            "discord_username": user.discord_username
        }
    }
    return func.HttpResponse(
        json.dumps(response),
        status_code=200
    )
