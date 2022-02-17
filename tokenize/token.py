import random
import hashlib
import os
from string import ascii_letters
from string import digits
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
from azure.core.exceptions import HttpResponseError
# Enryption Imports
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64

class Token:
    def __init__(self, customer: str, value: str):
        account_name = os.environ["accountName"]
        account_key = os.environ["accountKey"]
        self.key = base64.b64decode(os.environ["key"]) #b64encoded string
        if len(self.key) not in (16, 24, 32):
            raise ValueError("key must be 128, 192, or 256 bits.")

        endpoint = "https://{0}.table.core.windows.net/".format(account_name)
        self.credential = AzureNamedKeyCredential(account_name, account_key)
        self.table_service = TableServiceClient(endpoint=endpoint, credential=self.credential)
        key_table = "Keys"
        token_table = "Tokens"
        self.key_table_client = self.table_service.get_table_client(key_table)
        self.token_table_client = self.table_service.get_table_client(token_table)
        self.customer = customer
        self.raw_value = value

    def __del__(self):
        del self.key_table_client
        del self.token_table_client
        del self.table_service
        del self.credential
        del self.customer
        del self.raw_value

    def write_token_to_store(self, token_value: str):
        key_entity = self.write_key_entity(token_value)
        self.key_table_client.create_entity(key_entity)

    def write_key_entity_to_store(self, token_value: str):
        token_entity = self.write_token_entity(token_value)
        self.token_table_client.create_entity(token_entity)

    def write_key_entity(self, token_value: str) -> str:
        token = {
            "PartitionKey": self.customer,
            "RowKey": self.get_key(),
            "TokenValue": token_value,
            "RawValue": self.raw_value,
            "KeyType": 1,
        }
        return token

    def encrypt_raw_value(self, token_value: str) -> str:
        # Encrypt a message
        nonce = secrets.token_bytes(12)  # GCM mode needs 12 fresh bytes every time
        ciphertext = nonce + AESGCM(self.key).encrypt(nonce, token_value.encode(), b"")
        base64text = base64.b64encode(ciphertext)
        return  base64text.decode()

    def write_token_entity(self, token_value: str) -> dict:
        token = {
            "PartitionKey": self.customer,
            "RowKey": token_value,
            "Key": self.get_key(),
            "RawValue": self.encrypt_raw_value(self.raw_value),
            "KeyType": 2,
        }
        return token

    def get_token_value_from_store(self) -> str:
        try:
            key_entity = self.key_table_client.get_entity(
                partition_key=self.customer, row_key=self.get_key()
            )
            token_value = key_entity["TokenValue"]
        except HttpResponseError:
            token_value = None
        return token_value

    def get_key(self) -> str:
        m = hashlib.sha256()
        m.update(self.raw_value.encode())
        return m.hexdigest()

    def get_token_value(self) -> str:
        token_value = self.get_token_value_from_store()
        if token_value is None:
            token_value=self.generate_token_value()
            self.write_token_to_store(token_value)
            self.write_key_entity_to_store(token_value)
        else:
            token_value = token_value
        return token_value

    def generate_token_value(self) -> str:
        possible_values = ascii_letters
        if self.raw_value.isnumeric():
            possible_values = digits
        else:
            possible_values = ascii_letters
        token_value = "".join(
            random.choice(possible_values)
            for _ in range(len(self.raw_value))
        )
        return token_value
 