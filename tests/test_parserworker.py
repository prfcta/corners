import unittest
from parserworker2 import parserworker


class TestParserworkerLink(unittest.TestCase):
    def test_link(self):
        with self.assertRaises(TypeError) as e:
            parserworker(123)
        self.assertEqual("ссылка должна быть строкой", e.exception.args[0])


if __name__ == "__main__":
    unittest.main()








