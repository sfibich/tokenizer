import os
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
from azure.core.exceptions import HttpResponseError
# Enryption Imports
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64

class Detoken:
    def __init__(self, customer: str, token: str):
        account_name = os.environ["accountName"]
        account_key = os.environ["accountKey"]
        endpoint = "https://{0}.table.core.windows.net/".format(account_name)
        self.key = base64.b64decode(os.environ["key"]) #b64encoded string
        if len(self.key) not in (16, 24, 32):
            raise ValueError("key must be 128, 192, or 256 bits.")

        self.credential = AzureNamedKeyCredential(account_name, account_key)
        self.table_service = TableServiceClient(endpoint=endpoint, credential=self.credential)
        token_table = "Tokens"
        self.token_table_client = self.table_service.get_table_client(token_table)
        self.customer = customer
        self.token = token

    def __del__(self):
        del self.token_table_client
        del self.table_service
        del self.credential
        del self.customer
        del self.token

    def decrypt_raw_value(self,ciphertext64:str) -> str:
        ciphertext = base64.b64decode(ciphertext64)
        msg = AESGCM(self.key).decrypt(ciphertext[:12], ciphertext[12:], b"")
        return msg.decode()

    def get_value_from_store(self) -> str:
        try:
            token_entity = self.token_table_client.get_entity(
                partition_key=self.customer, row_key=self.token
            )
            ciphertext = token_entity["RawValue"]
            raw_value = self.decrypt_raw_value(ciphertext)
        except HttpResponseError:
            raw_value = None
        return raw_value
