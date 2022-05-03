import logging

import azure.functions as func

from discord import Webhook, RequestsWebhookAdapter

MOONRAKER_WEBHOOK_API_BTC = 'https://discord.com/api/webhooks/971034512068861972/gsCayDwdHOSMauUBNBcQiFHJObQ1nSXIRMScai6XUO3skyxzVpdJD0gV_oyhDzjTdXJ_'
MOONRAKER_WEBHOOK_API_ETH = 'https://discord.com/api/webhooks/971040197854773258/Wtw-TgnUM12_mDxByZzZ2Zeyq5dq9OmE-rosrOz_fLhVnQn30-nLB32WXDyfbX4y1xtm'


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
        
        if symbol == "BTCUSDT":
            webhook_api = MOONRAKER_WEBHOOK_API_BTC
        elif symbol == "ETHUSDT":
            webhook_api = MOONRAKER_WEBHOOK_API_ETH
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
            if moonraker_type == "Crossed Overboughtband":
                circle = ":red_circle:"
            elif moonraker_type == "Crossed Oversoldband":
                circle = ":green_circle:"
            else:
                return func.HttpResponse(
                    "The moonraker type is invalid.",
                    status_code=400
                )

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
