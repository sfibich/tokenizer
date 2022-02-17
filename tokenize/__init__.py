import logging
import json
import azure.functions as func
from . import token

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('tokenize function processed a request.')

    value = req.params.get('value')
    customer = req.params.get('customer')

    if value and customer:
        logging.debug('value and customer parameters provided')
        t = token.Token(customer=customer,value=value)
        logging.debug('token object created')
        token_value = t.get_token_value()
        logging.debug('token value gotten')
        return_value = {"token": token_value}
        logging.debug('returning value')
        return func.HttpResponse(json.dumps(return_value),mimetype="application/json")
    else:
        return func.HttpResponse(
            json.dumps({"message":"This HTTP triggered function executed successfully. Pass a value and customer in the query string to get the tokenized response."}),
            mimetype="application/json",
        )
