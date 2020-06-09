import unittest 
import os.path
from main import Scrape
from generateOptions import *

class MyTest(unittest.TestCase):

    def setUp(self):
        self.s = Scrape()

    def test_generate_options(self):
        # self.assertEqual(generate_options(), None)
        self.assertTrue(os.path.exists('resources/quote_sectors.json'))

    def test_get_dict_quoteSectors(self):
        d = {'SIC-7370 Services-Computer Programming, Data Processi': '-737A', 
             'Internet - Services': '-ITSE', 
             'Indices Nasdaq 100': '-INO', 
             'Indices S&P 100': '-ISO', 
             'Indices S&P 500': '-ISFI', 
             'Indices S&P 500 Telcomm': '-SAPL', 
             'Indices Nasdaq Composite': '-NASC', 
             'Indices Russell 1000': '-RUSO', 
             'Indices Russell 3000': '-RUSH'}
        self.assertEqual(self.s.get_dict_quoteSectors(), d)

    def test_infer(self):
        self.s.infer('resources/data.txt')
        self.assertTrue(os.path.exists('resources/Symbols.json'))

if __name__ == '__main__':
    unittest.main()