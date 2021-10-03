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

    def __init__(self,value,customer):
        account_name=os.environ["accountName"]
        account_key=os.environ["accountKey"]
        self.key_table = "Key"
        self.token_table = "Token"
        self.table_service = TableService(account_name=account_name, account_key=account_key)
        self.raw_value=value
        self.customer=customer
        self.key = self.get_key()
        self.token_value = self.get_token_value()

    def write_token_to_store(self):
        self.table_service.insert_entity(self.key_table,json.loads(self.token))

    def write_token2_to_store(self):
        self.table_service.insert_entity(self.token_table,json.loads(self.token2))

    def write_token(self, token_value:str) -> str:
        token = {
                "PartitionKey": self.customer,
                "RowKey":self.key,
                "TokenValue": token_value,
                "RawValue":self.raw_value,
                "KeyType":1
                }
        return json.dumps(token)

    def write_token2(self, token_value:str) -> str:
        token = {
                "PartitionKey": self.customer,
                "RowKey":token_value,
                "Key": self.key,
                "RawValue":self.raw_value,
                "KeyType":2
                }
        return json.dumps(token)

    def get_token_from_store(self):
        try:
            token1 = self.table_service.get_entity(self.key_table, self.customer,self.key)
            token_value=token1.TokenValue
        except AzureMissingResourceHttpError:
            token_value = None
        return token_value

    def get_key(self):
        m = hashlib.sha256()
        m.update(self.raw_value.encode())
        return m.hexdigest()

    def get_token_value(self):

        token_value = self.get_token_from_store()
        if (token_value is None):
            possible_values = ascii_letters
            if self.raw_value.isnumeric():
                possible_values = digits
            else:
                possible_values = ascii_letters

            token_value = ''.join(random.choice(possible_values) for _ in range(self.get_raw_value_length()))
            #need to test to see if token does not exist for customer...assume no for now.
            self.token = self.write_token(token_value)
            self.token2 = self.write_token2(token_value)
            self.write_token_to_store()
            self.write_token2_to_store()
        else:
            token_value = token_value

        return token_value

    def get_raw_value_length(self):
        return len(self.raw_value)

    def get_token_value_length(self):
        return len(self.token_value)
