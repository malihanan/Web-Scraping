﻿# Web Scraping
 This script scrapes the webpage: https://www.barchart.com/stocks/quotes/GOOG/competitors
 You can select a quote sector and the results on first page will be scraped and put into `Symbols.json` file.

### Powershell Scripts to run:

#### if running for the first time:
run `setup.ps1` to create virtual environment and install requirements.
#### running the script normally:
run `scrape.ps1`

### Files info
* data.txt to give input symbols
* generateOptions.py to fill generate_options.json file, runs in setup.ps1
* requirements.txt has all packages with their versions used
* scrape.py is the main script that does the scraping and generates outputs for input symbols
* test.py has unit test cases

##### Further extensions:
Can scrape for all quote sectors and all their pages (resource intensive)
