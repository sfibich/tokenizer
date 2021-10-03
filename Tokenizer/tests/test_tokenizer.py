import unittest
import json
import os

from Tokenize.token import Token

class TestTokenier(unittest.TestCase):

    def setUp(self):
        f=open("local.settings.json",)
        settingJson=json.load(f)
        os.environ["accountName"]=settingJson["Values"]["accountName"]
        os.environ["accountKey"]=settingJson["Values"]["accountKey"]
        f.close()

    def test_token_constructor(self):
        test_value = 'Test String'
        t = Token(test_value,"TestCustomer")
        self.assertEqual(t.raw_value,test_value)
        del t

    def test_token_get_token_not_equal(self):
        value = 'Here We Go'
        t = Token(value,"TestCustomer")
        self.assertNotEqual(t.get_token_value(),value)

    def test_token_get_token_length(self):
        value = 'Here We Go'
        t= Token(value,"TestCustomer")
        self.assertEqual(t.get_token_value_length(),len(value))

    def test_token_get_token_isnumeric(self):
        value ="12345"
        t =Token(value,"TestCustomer")
        token_value = t.get_token_value()
        self.assertTrue(token_value.isnumeric())

    def test_token_get_token_string_is_numeric(self):
        value = "Whatever"
        t = Token(value,"TestCustomer")
        token_value = t.get_token_value()
        self.assertFalse(token_value.isnumeric())

    def test_token_get_token_same_token_same_value(self):
        value = "Whatever"
        t = Token(value,"TestCustomer")
        token_value = t.get_token_value()
        token_value_2 = t.get_token_value()
        self.assertEqual(token_value,token_value_2)

    def test_token_get_key(self):
        value = "Whatever"
        t = Token(value,"TestCustomer")
        t2 = Token(value,"TestCustomer")
        self.assertEqual(t.get_key(), t2.get_key())

    def test_no_value_in_store(self):
        value = "Whatever2"
        t = Token(value,"TestCustomer")
        token = t.get_token_from_store()
        t2 = Token(value,"TestCustomer")
        token2 = t2.get_token_from_store()
        self.assertEqual(token,token2)

    def test_write_token(self):
        value = "Whatever3"
        t = Token(value,"TestCustomer")
        expected_token = {
                "PartitionKey":"TestCustomer",
                "RowKey":t.key,
                "TokenValue":t.token_value,
                "RawValue": value,
                "KeyType": 1
                }
        token = t.write_token(t.token_value)
        self.assertEqual(token,json.dumps(expected_token))
    '''
    def test_write_token2(self):
        value = "Whatever3.5"
        t = Token(value)
        expected_token = {
                "partitionKey":"TestCustomer",
                "rowKey":t.token_value,
                "key":t.key,
                "raw_value": value,
                "keyType": 2
                }
        token = t.write_token2(t.token_value)
        self.assertEqual(token,json.dumps(expected_token))
    '''
if __name__ == "__main__":
    unittest.main()
