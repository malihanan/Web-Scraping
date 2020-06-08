import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from pick import pick
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from generateOptions import *

class Scrape:

    url = "https://www.barchart.com/stocks/quotes/GOOG/competitors"

    def initializeDriver(self):
        self.timeout = 20

        #for headless chrome
        options = Options()
        options.headless = True
        options.add_argument('window-size=1200x600')
        options.add_argument(' — incognito')

        #accessing the url
        DRIVER_PATH = './chromedriver.exe'
        self.driver = webdriver.Chrome(options=options,
                                       executable_path=DRIVER_PATH)
        self.driver.get(self.url)

        print("Got", self.driver.current_url)

        # Wait 20 seconds for page to load
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.ID, 'competitors-quote-sectors')))
            return True
        except TimeoutException:
            print('Timed out waiting for options to load')
            self.end()
            return False

    def select(self):
        quoteSectors = get_dict_quoteSectors()

        title = 'Please choose a quote sector: '
        option, index = pick(list(quoteSectors.keys()), title)

        self.url = Scrape.url + "?quoteSectors=" + quoteSectors[option]

        print("Accessing", self.url)

    def scrape_table(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'bc-table-scrollable-inner')))
            return self.extract()
        except TimeoutException:
            print('Timed out waiting for table to load')
            self.end()

    def extract(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        #get all rows of the required table
        rows = soup.find(
            'div',
            class_='bc-table-scrollable-inner').find('tbody').find_all('tr')
        companies = []

        #iterate through table rows
        for i, row in enumerate(rows):
            #get symbols and names which are in separate td elements
            symbol = row.find('td', class_='symbol text-left').find('a').text
            name = row.find('td', class_='symbolName text-left').find(
                'span', attrs={
                    'data-ng-bind': 'cell'
                }).text
            #create a dict
            company = {'Symbol': symbol, 'Name': name}
            #append the dict in the list
            companies.append(company)

        #dump it in a json list
        json_list = json.loads(json.dumps(companies))
        return json_list

    def infer(self, fn):
        self.select()
        if self.initializeDriver():
            res = self.scrape_table()
            self.end()
            if res is not None:
                with open("Symbols.json", 'w') as f:
                    json.dump(res, f)
                found = []
                not_found = []
                with open(fn, 'r') as f:
                    symbols = f.read().split()
                    for symbol in symbols:
                        name = next(
                            (item["Name"] for item in res if item["Symbol"] == symbol),
                            None)
                        if name is not None:
                            found.append({symbol: name})
                        else:
                            not_found.append(symbol)
                ans = {'found': found, 'not_found': not_found}
                return json.loads(json.dumps(ans))

    def end(self):
        self.driver.quit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Give .txt file as an argument")
    else:
        s = Scrape()
        json_data = s.infer(sys.argv[1])
        x = pprint.pformat(json_data, indent=2, compact=True, width=50)
        print(x)