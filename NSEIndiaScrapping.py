# -*- coding: utf-8 -*-
"""
Created on Sat May 26 10:51:29 2018

@author: rushi
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json

url = 'https://www.nseindia.com/content/corporate/eq_research_reports_listed.htm#top'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html,'html5lib')
#print(soup.find(id='reportTbable'))
tableHeaderData = []
allTableData = []
allCompTable = soup.find(id='reportTbable')

for row in allCompTable.find_all('tr'):
    rowData = []
    for th in row.find_all('th'):
        tableHeaderData.append(th.get_text())
    for td in row.find_all('td'):
        rowData.append(td.get_text().replace('\n', '').replace('\xa0',''))
    npRowData = np.array(rowData)
    if npRowData.shape[0] > 0:
        allTableData.append(rowData)
    #print(row)
    
#print (allTableData)
#exit
nseDF = pd.DataFrame(allTableData,columns= tableHeaderData)
nseDF.drop(['Update 1','Update 2','Update 3','Update 4','Base Report'],axis=1,inplace = True)
#print(nseDF)
#print(nseDF.info())
#.add(['Last Price','Previous Close','Open','High','Low','Close'])
#nseDF['Last Price'] = []
#print(nseDF.info())
priceInfo = []
count = 0
for nseSymbol in nseDF['Symbol']:
    count += 1
    #if count == 2:
    #    break;
    #print(nseSymbol)
    print(count)
    rowPrice = []
    blankPrices = [nseSymbol,0,0,0,0,0,0]
    link = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+nseSymbol
    print(link)
    response = requests.get(link)
    html = response.content
    #print(html)
    soup = BeautifulSoup(html,'html5lib')
    #allCompTable = soup.find(id='reportTbable')
    #print(soup.find(id='responseDiv').get_text())
    if soup.find(id='responseDiv').get_text() == '':
        rowPrice = blankPrices
        
    else:
        d = json.loads(soup.find(id='responseDiv').get_text())
        #print(d['data'])
        if not d['data']:
            rowPrice = blankPrices
        else:
            rowPrice.append(nseSymbol)
            rowPrice.append(d['data'][0]['lastPrice'])
            rowPrice.append(d['data'][0]['previousClose'])
            rowPrice.append(d['data'][0]['open'])
            rowPrice.append(d['data'][0]['dayHigh'])
            rowPrice.append(d['data'][0]['dayLow'])
            rowPrice.append(d['data'][0]['closePrice'])
    #print(rowPrice)
    npRowPrice = np.array(rowPrice)
    if npRowPrice.shape[0] > 0 :
        priceInfo.append(rowPrice)
        
#print(priceInfo)
dfPrice = pd.DataFrame(priceInfo,columns = ['Symbol','Last Price','Previous Close','Open','Day High','Day Low','Close Price'] )
#print(dfPrice)
nseDF = pd.merge(nseDF,dfPrice,left_on='Symbol',right_on='Symbol',how='left')
print(nseDF)
nseDF.to_csv('nse_Data.csv', sep=',', encoding='utf-8')