import azure.functions as func
import json

from Get_User_By_Id.db_operations import getUserWithId

def main(req: func.HttpRequest) -> func.HttpResponse:

    userId = req.params.get('userId')
    if not userId:
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
            userId = req_body.get('userId')

    if not userId:
        response = {
            "success": "false",
            "msg": "User ID is not provided."
        }
        return func.HttpResponse(
            json.dumps(response),
            status_code=400
        )
    else:
        return getUserWithId(userId)
