
import azure.functions as func
import re
import json

from User_Registration.db_operations import checkIfEmailExists, registerUser


def main(req: func.HttpRequest) -> func.HttpResponse:

    email = req.params.get('email')
    password = req.params.get('password')
    discordUsername = req.params.get('discordUsername')

    if not (email and password and discordUsername):
        try:
            req_body = req.get_json()
        except ValueError:
            response = {
            "success": "false",
            "msg": "Bad Request."
            }
            return func.HttpResponse(
                json.dumps(response),
                status_code=400
            )
        else:
            email = req_body.get('email')
            password = req_body.get('password')
            discordUsername = req_body.get('discordUsername')

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
        response = validateEmail(email)
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
        response = validatePassword(password)
        if response is not None:
            return response
    if not discordUsername:
        response = {
            "success": "false",
            "msg": "Discord username is not provided."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )
    else:
        response = validateDiscordUsername(discordUsername)
        if response is not None:
            return response

    return registerUser(email, discordUsername, password)
            
                
def validateGender(gender):
    if (gender != 'Male' and gender != 'Female' and gender != 'Other' and gender != 'Prefer not to say' and gender != ''):
        response = {
            "success": "false",
            "msg": "Please select a valid gender."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )
    else:
        return None
    

def validateEmail(email):

    if checkIfEmailExists(email) == True:
        response = {
            "success": "false",
            "msg": "Email already exists."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(not (re.fullmatch(regex, email))):
        response = {
            "success": "false",
            "msg": "Invalid email."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )
    
    return None

def validatePassword(password):
    errorCode = -1
    responsemsg = [
        "Password is less than 8 characters",
        "Password must contain lower-case letters",
        "Password must contain uppercase letters",
        "Password must contain a number",
        "Password must contain a symbol",
        "Password must not contain whitespaces"
        ]
    isValid = True

    if (len(password) < 8):
        isValid = False
        errorCode = 0
    elif (not re.search("[a-z]", password)):
        isValid = False
        errorCode = 1
    elif not re.search("[A-Z]", password):
        isValid = False	
        errorCode = 2
    elif not re.search("[0-9]", password):
        isValid = False	
        errorCode = 3	
    elif not re.search("[_@$]", password):
        isValid = False
        errorCode = 4
    elif re.search("\s", password):
        isValid = False
        errorCode = 5
    
    if not isValid:
        errMsg = "Invalid Password - {}".format(responsemsg[errorCode])
        response = {
            "success": "false",
            "msg": errMsg
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )

    return None

def validateDiscordUsername(discordUsername):
    regex = r'^((.+?)#\d{4})'

    if(not (re.fullmatch(regex, discordUsername))):
        response = {
            "success": "false",
            "msg": "Invalid discord username."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )

    return None

