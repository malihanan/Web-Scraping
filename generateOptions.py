from bs4 import BeautifulSoup
import json

from scrape import *

def generate_options():
    s = Scrape()
    if s.initializeDriver():
        soup = BeautifulSoup(s.driver.page_source, 'lxml')
        #accessing the dropdown
        options = soup.find(id='competitors-quote-sectors').find_all('option')

        quoteSectors = {}
        for option in options:
            quoteSectors[option.text] = option['value']

        s.end()

        with open('quote_sectors.json', 'w') as f:
            json.dump(json.loads(json.dumps(quoteSectors)), f)

def get_dict_quoteSectors():
    with open('quote_sectors.json', 'r') as f:
        res = json.load(f)
    return res

if __name__ == '__main__':
    generate_options()