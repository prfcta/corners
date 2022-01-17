import unittest
from main.interface2 import select_choice
import sys
sys.path.append('C:\MyPythonProjects\Corners')


class SelectChoiceTest(unittest.TestCase):
    def test_selections(self):
        with self.assertRaises(ValueError) as e:
            select_choice('test')
        self.assertEqual('select_choice должен принимать словарь', e.exception.args[0])


if __name__ == "__main__":
    unittest.main()
    
    
