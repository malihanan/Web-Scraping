# Web Scraping
 This script scrapes the webpage: https://www.barchart.com/stocks/quotes/GOOG/competitors

 You can select a quote sector, the results on first page will be scraped and a list of Symbols and their Names will be put into `Symbols.json` file.

#### Download chromedriver.exe from https://sites.google.com/a/chromium.org/chromedriver/downloads and put in in the root folder of the project.
Refer https://chromedriver.chromium.org/downloads/version-selection to select correct version of chromedriver according to the version of your Chrome.

## Powershell Scripts to run:

#### `setup.ps1` creates virtual environment, installs requirements, generates options and runs `scrape.ps1`.
for first time run `scripts/setup.ps1` from root folder of project
You might have to run `Set-ExecutionPolicy RemoteSigned` before to enable running scripts.

#### `scrape.ps1` activates virtual environment and runs the main code.
run `scripts/scrape.ps1` from root folder of project to start scraping

### Directory Info
* src contains .py files
    * main.py is the main script that does the scraping and generates outputs for input symbols
    * generate_options.py fills resources/generate_options.json file that has all quote sectors, runs in setup.ps1
    * test.py has unit test cases
* scripts has scrape.ps1 and setup.ps1
* resources has text and json files generated
    * data.txt to give input symbols
    * requirements.txt has all required packages with versions for the script to run

#### Further extensions:
Can scrape for all quote sectors and all their pages (resource intensive)
