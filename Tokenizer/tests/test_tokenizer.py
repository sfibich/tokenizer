import unittest

class TestTokenier(unittest.TestCase):

    def test_raw(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == "__main__":
    unittest.main()
