from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#for headless chrome
options = Options()
options.headless = True

#accessing the url
DRIVER_PATH = './chromedriver.exe'	
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.barchart.com/stocks/quotes/GOOG/competitors")

#printing the title and url using WebDriver
print(driver.title)
print(driver.current_url)

#quit driver
driver.quit()