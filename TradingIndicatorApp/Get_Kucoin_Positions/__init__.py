import logging
import json

import azure.functions as func
from kucoin.client import Client


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    api_key = "624f0c96a2a59100017a52fe"
    api_secret = "ac976cb3-2c29-4a25-8a68-25eaed202ce6"
    passphrase = "Password123@"
    client = Client(api_key, api_secret, passphrase)
    positions = client.get_accounts(account_type="trade")
    
    result = []
    for p in positions:
        object = [p["currency"], p["balance"]]
        result.append(object)

    
    return func.HttpResponse(
            json.dumps(result),
            status_code=200
    )
