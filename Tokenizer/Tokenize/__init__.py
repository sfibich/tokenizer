import logging

import azure.functions as func
from Tokenize.token import Token

def main(req: func.HttpRequest, message: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    value = req.params.get('value')
    if not value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            value = req_body.get('value')

    if value:
        t = Token(value)
        message.set(t.token)
        return func.HttpResponse(t.token)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
