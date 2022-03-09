import logging

import azure.functions as func

from discord import Webhook, RequestsWebhookAdapter

MOONRAKER_WEBHOOK_API = 'https://discord.com/api/webhooks/904802607028125746/c5gTxZ7098A8DGVFGJn9ehdkr0TMxV4uQm6rgAqdWSwIKrsMtAi2ddcx88ZauuUNiKOU'

def main(req: func.HttpRequest) -> func.HttpResponse:

    symbol = req.params.get('symbol')
    time_interval = req.params.get('time-interval')
    moonraker_type = req.params.get('moonraker-type')


    if not symbol or not time_interval or not moonraker_type:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            symbol = req_body.get('symbol')
            time_interval = req_body.get('time-interval')
            moonraker_type = req_body.get('moonraker-type')

    if symbol and time_interval and moonraker_type:
        logging.info('Moonraker trigger function processed a request.')
        
        try:
            webhook = Webhook.from_url(MOONRAKER_WEBHOOK_API, adapter=RequestsWebhookAdapter())
        except ConnectionError:
            logging.error("Error with the discord connection!")
        else:
            logging.info('Webhook connected.')
            if moonraker_type == "Crossed Overboughtband":
                circle = ":red_circle:"
            elif moonraker_type == "Crossed Oversoldband":
                circle = ":green_circle:"

            webhook.send("{}  {}  {}  Moonraker - {}".format(circle, symbol, time_interval, moonraker_type))

            return func.HttpResponse(
                "Success",
                status_code=200
            )
        
    else:
        return func.HttpResponse(
             "There is a missing symbol, time interval or moonraker type in the request.",
             status_code=400
        )
