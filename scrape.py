from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

#for headless chrome
options = Options()
options.headless = True

#accessing the url
DRIVER_PATH = './chromedriver.exe'	
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.barchart.com/stocks/quotes/GOOG/competitors")

#get all rows of the required table
rows = driver.find_elements_by_xpath("//div[@class='bc-table-scrollable-inner']//tbody/tr")

companies = []

#iterate through table rows
for i,row in enumerate(rows):
    #get symbols and names which are in separate td elements
    symbol = row.find_element_by_xpath(".//td[@class='symbol text-left']//a").text
    name = row.find_element_by_xpath(".//td[@class='symbolName text-left']//span[@data-ng-bind='cell']").text
    #create a dict
    company = {'Symbol': symbol, 'Name': name}
    #append the dict in the list
    companies.append(company)

#dump it in a json list
json_list = json.dumps(companies)
print(json_list)

#quit driver
driver.quit()