from bs4 import BeautifulSoup
import json

from main import Scrape

def generate_options():
    s = Scrape()
    if s.initializeDriver():
        # Wait 20 seconds for page to load
        try:
            WebDriverWait(s.driver, s.timeout).until(EC.visibility_of_element_located((By.ID, 'competitors-quote-sectors')))
        except TimeoutException:
            print('Timed out waiting for options to load')
            s.end()
            
        soup = BeautifulSoup(s.driver.page_source, 'lxml')
        #accessing the dropdown
        options = soup.find(id='competitors-quote-sectors').find_all('option')
        s.end()

        quoteSectors = {}
        for option in options:
            quoteSectors[option.text] = option['value']

        with open('./../resources/quote_sectors.json', 'w') as f:
            json.dump(json.loads(json.dumps(quoteSectors)), f)
            print("Options successfully generated in resources/quote_sectors.json")

if __name__ == '__main__':
    generate_options()