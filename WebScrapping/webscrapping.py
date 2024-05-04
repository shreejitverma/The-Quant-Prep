#!/usr/bin/env python
# coding: utf-8

# <img src = 'img/logo.png' style = "height:70px; width:70px;float:right;"> 
# <h1><center> Webscrapping to MySQL</center></h1>
# 
# In this script we attempt to obtain market quotes from [investing.com](https://www.investing.com/). Despite there being an existent API from [investing.com](https://www.investing.com/) in Python (check out [`investpy`](https://pypi.org/project/investpy/)), this is a fun little project to introduce webscrapping with 2 important python packages: `Selenium` and `BeautifulSoup`.
# 
# Finally, we will do a quick overview of SQL and how to input the data we've scraped to MySQL. To do this, we will use the `mysql` package in Python.
# 
# `Selenium` is an API that allows us to use Selenium Webdriver to automate tasks on our browser. Using `selenium` we can direct our browser to specific pages where we want to scrape our data. 
# 
# `BeautifulSoup` on the other hand allows us to extract useful information from the pages we've obtained from `selenium`.
# 
# 
# ### Workflow
# 1. Set up selenium
# 2. Connect to [investing.com](https://www.investing.com/)
# 3. Parse HTML page using beautifulSoup
# 4. Store data in MySQL
# 
# <h2><center> 0. Import packages </center></h2>

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import time 
import pandas as pd
import os
from datetime import datetime as dt
import time
import itertools 

# Selenium Related packages
###############################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##SQL (pip install mysql-connector-python)
import mysql.connector


# <h2><center>1. Set up Selenium </center></h2>
# 
# ### Log in to investing.com

# In[2]:


# Investing login URL
url = 'https://www.investing.com'

# On ubuntu: sudo apt-get install chromium-chromedriver
# Connect to driver using Python
# Setting up options for WebDriver
driver = webdriver.Chrome()

# Connect to url
driver.get(url + '/login')

# Set up email and password to investing account
mail = 'calebmigosi@gmail.com' # lol mail me
password = PASSWORD

# Fill email
email = driver.find_element_by_id("loginFormUser_email")
email.clear()
email.send_keys(mail)

# Send Password
pwd = driver.find_element_by_id("loginForm_password")
pwd.clear()
pwd.send_keys(password)

# Click Sign in Button
driver.find_element_by_id("onetrust-accept-btn-handler").click()
driver.find_element_by_link_text("Sign In").click()

## Direct to Home Page
driver.get(url)


# ### Define pages of interest 

# In[3]:


#Regions of interest
regions = ['Americas', 'Europe', 'Asia/Pacific']
assetTypes = ['Indices', 'Stocks', 'ETFs', 'Bonds']


# In[4]:


def pageExtractor(region, assetType):
    driver.find_element_by_link_text("Markets").click()
    driver.find_element_by_link_text(region).click()
    driver.find_element_by_link_text(assetType).click()
    time.sleep(1)

    # Direct to main table and find the link on each
    wrapper = driver.find_elements_by_xpath("//div[@class = 'wrapper']")
    leftColumn = driver.find_element_by_id("leftColumn")

    content = leftColumn.find_element_by_css_selector("table[id = 'cross_rate_markets_indices_1']")
    overviewTable = content.find_elements_by_xpath("//table[@id = 'cross_rate_markets_indices_1']")
    tableElements = content.find_elements_by_xpath("//td[@class = 'bold left noWrap elp plusIconTd']")
    links = [elem.find_elements_by_tag_name("a")[0].get_attribute("href")
                for elem in tableElements]
    
    htmlPages = []
    for link in links:
        driver.get(link)
        driver.find_element_by_link_text("Historical Data").click()
        
        # Wait for page to load
        time.sleep(2)
        try:
            elem = driver.find_element_by_id("widgetFieldDateRange")
        except:
            print(link)
            next 
            
        # Change first date to 01/01/1970
        driver.find_element_by_id("widgetField").click()
        startDate = driver.find_element_by_id("startDate")
        startDate.clear()
        startDate.send_keys('01/01/1980')

        endDate = driver.find_element_by_id("endDate")
        endDate.clear()
        endDate.send_keys('01/01/2005')

        # Click apply button (Bit of an exception because of a JS element on the button)
        button = driver.find_element_by_xpath('//a[@id="applyBtn" and @class="newBtn Arrow LightGray float_lang_base_2"]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        htmlTable = []
        # Extract page as HTML
        htmlTable.append(BeautifulSoup(driver.page_source, 'html.parser'))

        # Change first date to 01/01/1970
        driver.find_element_by_id("widgetField").click()
        startDate = driver.find_element_by_id("startDate")
        startDate.clear()
        startDate.send_keys('01/01/2005')

        endDate = driver.find_element_by_id("endDate")
        endDate.clear()
        endDate.send_keys('01/01/2025')

        # Click apply button (Bit of an exception because of a JS element on the button)
        button = driver.find_element_by_xpath('//a[@id="applyBtn" and @class="newBtn Arrow LightGray float_lang_base_2"]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        # Extract page as HTML
        htmlTable.append(BeautifulSoup(driver.page_source, 'html.parser'))
        
        htmlPages.append(htmlTable)
        driver.find_element_by_link_text("Markets").click()
        driver.find_element_by_link_text(region).click()
        driver.find_element_by_link_text(assetType).click()
        
    return(htmlPages)


# <h2><center> 2. BeautifulSoup to extract quotes </center></h2>
# 
# Create a function to clean quotes from HTML and extract a table of quotes.

# In[5]:


def quoteExtractor(HTMLInput):
    # Find all table rows(tr) of a table 
    htmlTable = HTMLInput.find_all('tr')

    # Find text on the line
    quotes = [line.find_all(text = True) for line in htmlTable]

    # If 'No results found' return NA
    quoteStr = [' '.join(quote) for quote in quotes]
    if '\n No results found \n' in quoteStr: return(pd.DataFrame([]))

    # Select either dates or numbers(quotes)
    regexQuotes =  re.compile(r'([A-Za-z]{3} [0-9]{2})|([0-9.]{1,20})')
    regexDates =  re.compile(r'([A-Za-z]{3} [0-9]{2})')
    reg = re.compile(r'^(?!\n$)')

    'Extract quotes as nested list'
    quoteList = []
    # Filter out dates and quotes in each row
    for row in quotes:
        quote = list(filter(reg.match, row))     # Remove \n strings
        quoteList.append(list(filter(regexQuotes.match, quote)))

    # Remove Empty Lists
    quoteList = list(filter(None, quoteList))

    'Find column names'
    # Find column headers by class
    colnames = [line.find_all('th', 
                              {"class": {"noWrap pointer", "first left noWrap pointer"}}) for line in htmlTable]

    # Remove empty classes 
    colnames = list(filter(None, colnames))
    cols = [line.find_all(text = True) for line in colnames[0]]

    # Find field names
    fields = list(itertools.chain(*cols))

    'Assign column names to columns'
    # Select only the first 6 columns
    quoteData = pd.DataFrame(quoteList)
    quoteData.columns = fields 

    validRows = list(filter(regexDates.match, quoteData['Date']))
    validDates = [(quote in validRows) for quote in quoteData['Date']]

    # Filter out by valid dates
    quoteData = quoteData[validDates]

    # Set Dates as index
    quoteData.Date = [dt.strptime(re.sub(',', '', date), '%b %d %Y') for date in quoteData.Date]

    # Change Close, Open, High and Low columns
    # Change quotes from strings to floats
    quoteCleaner = lambda x: [float(re.sub(",", "", quote)) for quote in  x]
    quoteData[['Price', 'Open', 'High', 'Low']] = quoteData[['Price', 'Open', 'High', 'Low']].apply(quoteCleaner)
    
    return quoteData[['Date', 'Price', 'Open', 'High', 'Low']]


# <h2><center> 3. Data into SQL </center></h2>
# 
# ### Create market data schema

# In[6]:


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="xj6yFfEtOA3NjaLT*tx0"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE market_data")

# Connect to marker_data
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password= PASSWORD,
  database = 'market_data')

mycursor = mydb.cursor()


# ### Create data tables

# In[7]:


# Stock Quote Table Function
def tableCreator(table_name, colnames, coltype):
    '''Concatenate the commands'''
    sqlCommand = "CREATE TABLE "+ table_name +" ("
    columnDefs = [colname +" "+ coltype for colname, coltype in zip(colnames, coltype)]
    columnDefs = ", ".join(columnDefs)

    # Execute commands
    mycursor.execute(sqlCommand + columnDefs  + ')')
    
    print(table_name + ' created.')


# #### Stock and ETF Quote Table

# In[8]:


# Create stock quote parameters
colnames = ['id', 'name', 'asset_id', 'Close', 'Open', 'High', 'Low', 'Volume']
coltypes = ['INT AUTO_INCREMENT PRIMARY KEY NOT NULL', 'DATE NOT NULL', 'INT',
           'DECIMAL(20,6)',
           'DECIMAL(20,6)',
           'DECIMAL(20,6)',
           'DECIMAL(20,6)','INT']

# Create stock quotes
tableCreator('stock_quotes', colnames, coltypes)
tableCreator('index_quotes', colnames, coltypes)
tableCreator('etf_quotes', colnames, coltypes)
tableCreator('commodity_quotes', colnames, coltypes)
tableCreator('crypto_quotes', colnames, coltypes)


# #### Other Asset Quote Table

# In[9]:


# Create stock quote parameters
colnames = ['id', 'name', 'asset_id', 'Close', 'Open', 'High', 'Low']
coltypes = ['INT AUTO_INCREMENT PRIMARY KEY NOT NULL', 'DATE NOT NULL', 'INT',
           'DECIMAL(20,6)',
           'DECIMAL(20,6)',
           'DECIMAL(20,6)',
           'DECIMAL(20,6)']

# Create stock quotes
tableCreator('forex_quotes', colnames, coltypes)
tableCreator('bond_yield_quotes', colnames, coltypes)


# #### Fund Quote Table

# In[10]:


# Create stock quote parameters
colnames = ['id', 'name', 'asset_id', 'NAV']
coltypes = ['INT AUTO_INCREMENT PRIMARY KEY NOT NULL', 'DATE NOT NULL', 'INT',
           'DECIMAL(20,6)']

# Create stock quotes
tableCreator('fund_quotes', colnames, coltypes)


# #### Stock and ETF Static Data

# In[11]:


# Create stock quote parameters
colnames = ['id', 'name', 'Ticker', 'Industry', 'Sector', 'Beta', 'EPS', 'Shares']
coltypes = ['INT AUTO_INCREMENT PRIMARY KEY NOT NULL', 
           'VARCHAR(45)',
           'VARCHAR(45)',
           'VARCHAR(45)',
           'VARCHAR(45)',
           'DECIMAL(8,6)',
           'DECIMAL(10,6)',
           'INT']

# Create stock quotes
tableCreator('stock_details', colnames, coltypes)
tableCreator('etf_details', colnames, coltypes)


# #### Bond Spread Data (vs Bund)

# In[12]:


# Create stock quote parameters
colnames = ['id', 'name', 'asset_id', 'NAV']
coltypes = ['INT AUTO_INCREMENT PRIMARY KEY NOT NULL', 'DATE NOT NULL', 'INT',
           'DECIMAL(20,6)']

# Create stock quotes
tableCreator('bond_spread_quotes', colnames, coltypes)

