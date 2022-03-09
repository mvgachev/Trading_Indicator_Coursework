import logging

import azure.functions as func

from discord import Webhook, RequestsWebhookAdapter

PREDATOR_WEBHOOK_API = 'https://discord.com/api/webhooks/904802607028125746/c5gTxZ7098A8DGVFGJn9ehdkr0TMxV4uQm6rgAqdWSwIKrsMtAi2ddcx88ZauuUNiKOU'

def main(req: func.HttpRequest) -> func.HttpResponse:

    symbol = req.params.get('symbol')
    time_interval = req.params.get('time-interval')
    terminator_type = req.params.get('terminator-type')


    if not symbol or not time_interval or not terminator_type:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            symbol = req_body.get('symbol')
            time_interval = req_body.get('time-interval')
            terminator_type = req_body.get('terminator-type')

    if symbol and time_interval and terminator_type:
        logging.info('Terminator trigger function processed a request.')
        
        try:
            webhook = Webhook.from_url(PREDATOR_WEBHOOK_API, adapter=RequestsWebhookAdapter())
        except ConnectionError:
            logging.error("Error with the discord connection!")
        else:
            logging.info('Webhook connected.')
            if terminator_type == "Bear div":
                circle = ":red_circle:"
            elif terminator_type == "Bull div":
                circle = ":green_circle:"

            webhook.send("{}  {}  {}  Terminator - {}".format(circle, symbol, time_interval, terminator_type))

            return func.HttpResponse(
                "Success",
                status_code=200
            )
        
    else:
        return func.HttpResponse(
             "There is a missing symbol, time interval or terminator type in the request.",
             status_code=400
        )
