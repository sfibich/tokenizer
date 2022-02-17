import unittest
import json
import os
from azure.common import AzureConflictHttpError

from Tokenize.token import Token

class TestTokenier(unittest.TestCase):

    def setUp(self):
        f=open("local.settings.json",)
        settingJson=json.load(f)
        os.environ["accountName"]=settingJson["Values"]["accountName"]
        os.environ["accountKey"]=settingJson["Values"]["accountKey"]
        f.close()

    def test_token_constructor(self):
        test_value = 'Test8String'
        t = Token(test_value,"TestCustomer")
        self.assertEqual(t.raw_value,test_value)
        self.assertEqual(t.customer,"TestCustomer")

    def test_get_key(self):
        test_value = 'Test8String'
        t= Token(test_value,"t22")
        self.assertEqual(t.get_key(),"10facb75247755cd13c2a292191c7d9e8e815287619e3491bb30c31e7057c198")

    def test_get_token_from_store_none(self):
        test_value = 'Test9String'
        t= Token(test_value,"TestCustomer")
        token_value= t.get_token_from_store()
        self.assertIsNone(token_value)

    def test_get_token_from_store_true(self):
        test_value = 'Test10String'
        t=Token(test_value,"TestCustomer")
        from azure.cosmosdb.table.tableservice import TableService
        from azure.cosmosdb.table.models import Entity

        account_name=os.environ["accountName"]
        account_key=os.environ["accountKey"]
        key_table = "Key"
        token_table = "Token"
        table_service = TableService(account_name=account_name, account_key=account_key)
        token = {
                "PartitionKey": t.customer,
                "RowKey": t.get_key(),
                "TokenValue": "TEST",
                "RawValue":t.raw_value,
                "KeyType":1
                }
        token_string=json.dumps(token)
        try:
            table_service.insert_entity(key_table,json.loads(token_string))
        except AzureConflictHttpError:
            pass

        token_actual = t.get_token_from_store()
        ## CLEAN UP ##
        table_service.delete_entity(key_table, t.customer, t.get_key())

        self.assertEqual(token_actual,token["TokenValue"])


if __name__ == "__main__":
    unittest.main()
