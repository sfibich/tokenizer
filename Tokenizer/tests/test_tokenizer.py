import unittest
import json

from Tokenize.token import Token

class TestTokenier(unittest.TestCase):

    def test_token_constructor(self):
        test_value = 'Test String'
        t = Token(test_value)
        self.assertEqual(t.raw_value,test_value)

    def test_token_get_token_not_equal(self):
        value = 'Here We Go'
        t = Token(value)
        self.assertNotEqual(t.get_token_value(),value)

    def test_token_get_token_length(self):
        value = 'Here We Go'
        t= Token(value)
        self.assertEqual(t.get_token_value_length(),len(value))

    def test_token_get_token_isnumeric(self):
        value ="12345"
        t =Token(value)
        token_value = t.get_token_value()
        self.assertTrue(token_value.isnumeric())

    def test_token_get_token_string_is_numeric(self):
        value = "Whatever"
        t = Token(value)
        token_value = t.get_token_value()
        self.assertFalse(token_value.isnumeric())

    def test_token_get_token_same_token_same_value(self):
        value = "Whatever"
        t = Token(value)
        token_value = t.get_token_value()
        token_value_2 = t.get_token_value()
        self.assertEqual(token_value,token_value_2)

    def test_token_get_key(self):
        value = "Whatever"
        t = Token(value)
        t2 = Token(value)
        self.assertEqual(t.get_key(), t2.get_key())

    def test_no_value_in_store(self):
        value = "Whatever2"
        t = Token(value)
        token = t.get_token_from_store()
        t2 = Token(value)
        token2 = t2.get_token_from_store()
        self.assertEqual(token,token2)

    def test_write_token(self):
        value = "Whatever3"
        t = Token(value)
        expected_token = {
                "partitionKey":"TestCustomer",
                "rowKey":t.key,
                "token_value":t.token_value,
                "raw_value": value,
                "keyType": 1
                }
        token = t.write_token()
        self.assertEqual(token,json.dumps(expected_token))

    def test_write_token_to_store(self):
        value = "Whatever4"
        t = Token(value)
        t.write_token_to_store()
        try:
            token = Token.tokens[t.key]
        except KeyError:
            self.fail("no token")


if __name__ == "__main__":
    unittest.main()
