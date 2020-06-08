import unittest 
from scrape import Scrape
from generateOptions import *

class MyTest(unittest.TestCase):

    def setUp(self):
        self.s = Scrape()

    def test_generate_options(self):
        self.assertEqual(generate_options(), None)

    def test_get_dict_quoteSectors(self):
        self.assertEqual(get_dict_quoteSectors(), '')

    def test_init_driver(self):
        self.assertEqual(self.s.initializeDriver(), True)

if __name__ == '__main__':
    unittest.main()