import logging

import azure.functions as func

from discord import Webhook, RequestsWebhookAdapter

PREDATOR_WEBHOOK_API_BTC = 'https://discord.com/api/webhooks/904802607028125746/c5gTxZ7098A8DGVFGJn9ehdkr0TMxV4uQm6rgAqdWSwIKrsMtAi2ddcx88ZauuUNiKOU'
PREDATOR_WEBHOOK_API_ETH = 'https://discord.com/api/webhooks/971039743259336744/0GEquCKfJ7lmCk2nVif1nuon4fei0n9NdcZt6PLAhQtkmdA6-9LIjqB06MD1rzGw-dU3'

def main(req: func.HttpRequest) -> func.HttpResponse:

    symbol = req.params.get('symbol')
    time_interval = req.params.get('time-interval')
    predator_type = req.params.get('predator-type')


    if not symbol or not time_interval or not predator_type:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            symbol = req_body.get('symbol')
            time_interval = req_body.get('time-interval')
            predator_type = req_body.get('predator-type')

    if symbol and time_interval and predator_type:
        logging.info('Predator trigger function processed a request.')
        
        if symbol == "BTCUSDT":
            webhook_api = PREDATOR_WEBHOOK_API_BTC
        elif symbol == "ETHUSDT":
            webhook_api = PREDATOR_WEBHOOK_API_ETH
        else:
            return func.HttpResponse(
                "The symbol is not supported yet.",
                status_code=400
            )

        try:
            webhook = Webhook.from_url(webhook_api, adapter=RequestsWebhookAdapter())
        except ConnectionError:
            logging.error("Error with the discord connection!")
        else:
            logging.info('Webhook connected.')
            if predator_type == "Short Signal" or predator_type == "Stopped Out of Long":
                circle = ":red_circle:"
            elif predator_type == "Long Signal" or predator_type == "Stopped Out of Short":
                circle = ":green_circle:" 
            else:
                return func.HttpResponse(
                    "The predator type is invalid.",
                    status_code=400
                )               

            webhook.send("{}  {}  {}  Predator - {}".format(circle, symbol, time_interval, predator_type))

            return func.HttpResponse(
                "Success",
                status_code=200
            )
        
    else:
        return func.HttpResponse(
             "There is a missing symbol, time interval or predator type in the request.",
             status_code=400
        )
