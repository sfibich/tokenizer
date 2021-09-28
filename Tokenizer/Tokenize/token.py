import random
import hashlib
import json
import os
from azure.common import AzureMissingResourceHttpError
from string import ascii_letters
from string import digits
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity


class Token():
    tokens = {}

    def __init__(self,value):
        account_name=os.environ["accountName"]
        account_key=os.environ["accountKey"]
        self.table_service = TableService(account_name=account_name, account_key=account_key)
        self.raw_value=value
        self.customer="TestCustomer"
        self.key = self.get_key()
        self.token_value = self.get_token_value()
        self.token = self.write_token()
        self.write_token_to_store()

    def write_token_to_store(self):
        #Token.tokens[self.key] = self.token
        pass

    def write_token(self):
        token = {
                "partitionKey": self.customer,
                "rowKey":self.key,
                "token_value": self.token_value,
                "raw_value":self.raw_value,
                "keyType":1
                }
        return json.dumps(token)

    def write_token2(self):
        token = {
                "partitionKey": self.customer,
                "rowKey":self.token_value,
                "key": self.key,
                "raw_value":self.raw_value,
                "keyType":2
                }
        return json.dumps(token)

    def get_token_from_store(self):
        try:
            token1 = self.table_service.get_entity('test', self.customer,self.key)
            token=token1.rowKey
        except AzureMissingResourceHttpError:
            token = None
        return token

    def get_key(self):
        m = hashlib.sha256()
        m.update(self.raw_value.encode())
        return m.hexdigest()

    def get_token_value(self):

        self.token = self.get_token_from_store()
        if (self.token is None):
            possible_values = ascii_letters
            if self.raw_value.isnumeric():
                possible_values = digits
            else:
                possible_values = ascii_letters

            token_value = ''.join(random.choice(possible_values) for _ in range(self.get_raw_value_length()))
        else:
            token_value = json.loads(self.token)["token_value"]

        return token_value

    def get_raw_value_length(self):
        return len(self.raw_value)

    def get_token_value_length(self):
        return len(self.token_value)
