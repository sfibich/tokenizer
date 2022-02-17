import logging
import json
import azure.functions as func
from . import detoken

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('detokenize function processed a request.')

    token = req.params.get('token')
    customer = req.params.get('customer')

    if token and customer:
        raw_value = detoken.Detoken(customer=customer, token=token)
        value=raw_value.get_value_from_store()
        return_value = {"value": value}      
        return func.HttpResponse(json.dumps(return_value),mimetype="application/json")
    else:
        return func.HttpResponse(
            json.dumps({"message":"This HTTP triggered function executed successfully. Pass a value and customer in the query string to get the detokenized response."}),
            mimetype="application/json",
        )
