from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from main import Scrape

def generate():
    print("Generating options")
    s = Scrape()
    s.initializeDriver()
    print("Driver Initialized")
    # Wait 20 seconds for page to load
    try:
        WebDriverWait(s.driver, s.timeout).until(EC.visibility_of_element_located((By.ID, 'competitors-quote-sectors')))
        soup = BeautifulSoup(s.driver.page_source, 'lxml')
        #accessing the dropdown
        options = soup.find(id='competitors-quote-sectors').find_all('option')
        s.end()

        quoteSectors = {}
        for option in options:
            quoteSectors[option.text] = option['value']

        with open('resources/quote_sectors.json', 'w') as f:
            json.dump(json.loads(json.dumps(quoteSectors)), f)
            print("Options successfully generated in resources/quote_sectors.json")

    except TimeoutException:
        print('Timed out waiting for options to load. Check your Internet Connection.')
        s.end()

if __name__ == '__main__':
    generate()