from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#for headless chrome
options = Options()
options.headless = True

#accessing the url
DRIVER_PATH = './chromedriver.exe'	
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.barchart.com/stocks/quotes/GOOG/competitors")

#get all rows of the required table
rows = driver.find_elements_by_xpath("//div[@class='bc-table-scrollable-inner']//tbody/tr")

#get and print symbols and names which are in separate td elements
for i,row in enumerate(rows):
	symbol = row.find_element_by_xpath(".//td[@class='symbol text-left']//a").text
	name = row.find_element_by_xpath(".//td[@class='symbolName text-left']//span[@data-ng-bind='cell']").text
	print(symbol, "-", name)

#quit driver
driver.quit()