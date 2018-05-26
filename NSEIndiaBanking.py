# -*- coding: utf-8 -*-
"""
Created on Sat May 26 19:25:51 2018

@author: rushi
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

url = 'http://www.moneycontrol.com/india/stockmarket/sector-classification/marketstatistics/nse/banking-finance.html'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html,'html5lib')
bankTable = soup.find_all('table',{'class':'bdrtpg'})
headerData = []
allTableData = []
for tr in bankTable[0].find_all('tr'):
    rowData = []
    for th in tr.find_all('th'):
        headerData.append(th.get_text())
    for td in tr.findAll('td'):
        rowData.append(td.get_text())
    npRowData = np.array(rowData)
    if npRowData.shape[0] > 0:
        allTableData.append(rowData)
        
#print(allTableData)
bankDataDF = pd.DataFrame(allTableData,columns = headerData)

bankDataDF['Last Price'] = bankDataDF['Last Price'].astype(np.float)
bankDataDF['Change'] = bankDataDF['Change'].astype(np.float)
bankDataDF['%Chg'] = bankDataDF['%Chg'].astype(np.float)
bankDataDF['Mkt Cap(Rs cr)'].replace(to_replace = ',',value='',inplace = True,regex=True)
bankDataDF['Mkt Cap(Rs cr)'] = bankDataDF['Mkt Cap(Rs cr)'].astype(np.float)
print(bankDataDF.info()) 

#bankDataDF.to_csv('nseBankData.csv',sep=',', encoding='utf-8')

#print()
finalDF = bankDataDF.groupby(by='Industry',axis=0).agg({'Company Name':'count', 'Mkt Cap(Rs cr)': 'sum'}).reset_index()
#print(finalDF)
fig, axes = plt.subplots(nrows=1, ncols=2)
axes[0].bar(finalDF['Industry'],finalDF['Company Name'])

axes[1].bar(finalDF['Industry'],finalDF['Mkt Cap(Rs cr)'])
fig.tight_layout()
plt.show()
