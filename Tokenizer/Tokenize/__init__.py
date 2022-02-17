import logging

import azure.functions as func
from Tokenize.token import Token

def main(req: func.HttpRequest) -> func.HttpResponse:
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
        return func.HttpResponse(t.token)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Please passa value to tokenize.",
             status_code=200
        )
