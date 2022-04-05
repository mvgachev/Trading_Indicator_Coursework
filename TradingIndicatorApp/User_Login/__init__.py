import json
import logging

import azure.functions as func
from User_Login.db_operations import checkIfPasswordMatch

from User_Registration.db_operations import checkIfEmailExists, getUserId, getUserWithEmail
import logging



def main(req: func.HttpRequest) -> func.HttpResponse:

    email = req.params.get('email')
    password = req.params.get('password')
    if not (email and password):
        try:
            req_body = req.get_json()
        except ValueError:
            response = {
            "success": "false",
            "msg": "Bad Request"
            }
            return func.HttpResponse(
                json.dumps(response),
                status_code=400
            )
        else:
            email = req_body.get('email')
            password = req_body.get('password')

    if not email:
        response = {
            "success": "false",
            "msg": "Email is not provided."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )
    else:
        response = checkEmail(email)
        if response is not None:
            return response
    if not password:
        response = {
            "success": "false",
            "msg": "Password is not provided."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )
    else:
        return checkPassword(password, email)
            

def checkEmail(email):

    if checkIfEmailExists(email) == False:
        logging.info("Email does not exist.")
        response = {
            "success": "false",
            "msg": "User with this email does not exist."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=401
        )
    else:
        return None

def checkPassword(password, email):

    if checkIfPasswordMatch(password, email) == False:

        response = {
            "success": "false",
            "msg": "Password is incorrect"
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=401
        )
    else:
        user = getUserWithEmail(email)
        response = {
            "success": "true",
            "msg": "You have logged in successfully.",
            "user": {
                "id": user.id,
                "email": email,
                "discord_username": user.discord_username
            }
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=200
        )                


