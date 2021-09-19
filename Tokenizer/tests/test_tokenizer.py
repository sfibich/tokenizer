import unittest
from Tokenize.token import Token

class TestTokenier(unittest.TestCase):

    def test_token_constructor(self):
        test_value = 'Test String'
        t = Token(test_value)
        self.assertEqual(t.raw_value,test_value)

    def test_token_get_token_not_equal(self):
        value = 'Here We Go'
        t = Token(value)
        self.assertNotEqual(t.get_token(),value)

    def test_token_get_token_length(self):
        value = 'Here We Go'
        t= Token(value)
        self.assertEqual(t.get_token_value_length(),len(value))

    def test_token_get_token_isnumeric(self):
        value ="12345"
        t =Token(value)
        token_value = t.get_token()
        self.assertTrue(token_value.isnumeric())

    def test_token_get_token_string_is_numeric(self):
        value = "Whatever"
        t = Token(value)
        token_value = t.get_token()
        self.assertFalse(token_value.isnumeric())

    def test_token_get_token_same_token_same_value(self):
        value = "Whatever"
        t = Token(value)
        token_value = t.get_token()
        token_value_2 = t.get_token()
        self.assertEqual(token_value,token_value_2)


if __name__ == "__main__":
    unittest.main()
