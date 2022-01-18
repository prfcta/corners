import unittest
from parserworker2 import create_links_with_id

class TestCreateLinksWithId(unittest.TestCase):
    def test_string_id_box_is_tuple_(self):
        with self.assertRaises(TypeError) as e:
            create_links_with_id('123')
            
    def test_integer_id_box_is_tuple(self):
        with self.assertRaises(TypeError) as e:
            create_links_with_id(123)








if __name__ == "__main__":
    unittest.main()