import logging

import azure.functions as func

from discord import Webhook, RequestsWebhookAdapter

TERMINATOR_WEBHOOK_API_BTC = 'https://discord.com/api/webhooks/971034686107291668/aHGvtfBGqZb1t14uTTPcly9gu_nkefTlB3DvzMLxOQqAcmahhqXDDsyoJnXH0MjBhZIY'
TERMINATOR_WEBHOOK_API_ETH = 'https://discord.com/api/webhooks/971040734427893801/ChIdO1wWo-usHR-RurklzxB-_ahKQUlerVypb6oQqYFoqmYKN21popOyrFdFQMPmcjEt'


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
        
        if symbol == "BTCUSDT":
            webhook_api = TERMINATOR_WEBHOOK_API_BTC
        elif symbol == "ETHUSDT":
            webhook_api = TERMINATOR_WEBHOOK_API_ETH
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
            if terminator_type == "Bear div":
                circle = ":red_circle:"
            elif terminator_type == "Bull div":
                circle = ":green_circle:"
            else:
                return func.HttpResponse(
                    "The terminator type is invalid.",
                    status_code=400
                )

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
