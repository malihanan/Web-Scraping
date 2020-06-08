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
        self.driver.get(Scrape.url)

        # Wait 20 seconds for page to load
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.ID, 'competitors-quote-sectors')))
        except TimeoutException:
            print('Timed out waiting for options to load')
            self.end()

    def select(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        #accessing the dropdown
        # self.wait.until(EC.visibility_of_element_located((By.ID, "#competitors-quote-sectors")))
        options = soup.find(id='competitors-quote-sectors').find_all('option')

        quoteSectors = {}
        names = []
        for option in options:
            quoteSectors[option.text] = option['value']
            names.append(option.text)

        title = 'Please choose a quote sector: '
        option, index = pick(names, title)

        #clicking on the selected option
        path = "//select[@id='competitors-quote-sectors']/option[@value='" + quoteSectors[option] + "']"
        try:
            self.driver.find_element_by_xpath(path).click()
        except:
            print("Refreshing page...")
            self.driver.refresh()
            try:
                WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, path)))
            except TimeoutException:
                print('Timed out waiting for options to load after refreshing')
                self.end()

    def scrape_table(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        #get all rows of the required table
        # self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bc-table-scrollable-inner")))
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'bc-table-scrollable-inner')))
        except TimeoutException:
            print('Timed out waiting for table to load')
            print("Refreshing page...")
            self.driver.refresh()
            try:
                WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'bc-table-scrollable-inner')))
            except TimeoutException:
                print('Timed out waiting for table to load after refreshing')
                self.end()

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

    def end(self):
        self.driver.quit()

    def infer(self, fn):
        self.initializeDriver()
        self.select()
        res = self.scrape_table()
        with open("Symbols.json", 'w') as f:
            json.dump(res, f)
        self.end()
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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Give .txt file as an argument")
    else:
        s = Scrape()
        json_data = s.infer(sys.argv[1])
        x = pprint.pformat(json_data, indent=2, compact=True, width=50)
        print(x)