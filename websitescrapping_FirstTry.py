# -*- coding: utf-8 -*-
"""
Created on Fri May 25 12:27:58 2018

@author: rushi
"""

import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#url = 'https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India'
url = 'https://coinmarketcap.com/all/views/all/'
response = requests.get(url)
html = response.content
#print(html)

soup = BeautifulSoup(html,'html5lib')
#print(soup)
table = soup.find_all('table')
print(len(table))
#print(table)
table1 = table[0]
rows = table1.find_all('tr')
indexs = []
allValues = []
print(len(rows))
for row in table1.find_all('tr'):
    values = []
    for head in row.find_all('th'):
        #print(head.get_text())
        indexs.append(head.get_text())
    for vals in row.find_all('td'):
        values.append(vals.get_text().replace('\n',''))
    npValues = np.array(values)
    if npValues.shape[0] >0:
        allValues.append(values)
dataFrame = pd.DataFrame(allValues,columns = indexs)
dataFrame.drop(columns='',inplace = True)
dataFrame['Market Cap'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['Market Cap'].replace(to_replace = '[$,]',value = '',inplace = True,regex = True)
dataFrame['Market Cap'] = dataFrame['Market Cap'].astype(float)

dataFrame['Price'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['Price'].replace(to_replace = '[$,]',value = '',inplace = True,regex = True)
dataFrame['Price'] = dataFrame['Price'].astype(float)

dataFrame['Circulating Supply'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['Circulating Supply'].replace(to_replace = '[$,*]',value = '',inplace = True,regex = True)
dataFrame['Circulating Supply'] = dataFrame['Circulating Supply'].astype(float)

dataFrame['Volume (24h)'].replace(to_replace = 'Low Vol*',value = '0',inplace = True,regex=True)
dataFrame['Volume (24h)'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['Volume (24h)'].replace(to_replace = '[$,*]',value = '',inplace = True,regex = True)
dataFrame['Volume (24h)'] = dataFrame['Volume (24h)'].astype(float)

dataFrame['% 1h'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['% 1h'].replace(to_replace = '[$,*%]',value = '',inplace = True,regex = True)
dataFrame['% 1h'] = dataFrame['% 1h'].astype(float)

dataFrame['% 24h'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['% 24h'].replace(to_replace = '[$,*%]',value = '',inplace = True,regex = True)
dataFrame['% 24h'] = dataFrame['% 24h'].astype(float)

dataFrame['% 7d'].replace(to_replace = '[?]',value = '0',inplace = True,regex = True)
dataFrame['% 7d'].replace(to_replace = '[$,*%]',value = '',inplace = True,regex = True)
dataFrame['% 7d'] = dataFrame['% 7d'].astype(float)

print(dataFrame.info())
#print(dataFrame)
dataFrame['Name'].replace(to_replace = dataFrame['Symbol'],value = '',inplace = True,regex = True)
print(dataFrame.head())