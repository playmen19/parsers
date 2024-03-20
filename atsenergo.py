import os
import datetime
import pandas as pd
import numpy as np
import statistics
import requests, urllib
from bs4 import BeautifulSoup as bs
from threading import Thread
os.chdir("C:/Users/playmen/source/python/atsenergo/data")

ids = []
soup = bs(urllib.request.urlopen('http://www.atsenergo.ru/results/market/calcfacthour'))
options = soup.find_all("option")
for option in options:
    id = option["value"]
    ids.append(id)
    ids = list(filter(lambda x: len(x) > 0, ids))
    
links = []
for x in range(len(ids)):
    data = urllib.parse.urlencode({"data": "results/market/calcfacthour", "id": ids[x]})
    data = data.encode('ascii')
    soup = bs(urllib.request.urlopen('https://www.atsenergo.ru/js-data', data))
    hrefs = soup.find_all("a")
    for link in hrefs:
        prom = link["href"]
        if prom.endswith(".xls"):
             links.append(prom)

def download(x, links):
    urllib.request.urlretrieve(links[x], links[x][52:])

for x in range (len(links)):
    mainThread = Thread(target = download, args = (x, links,))
    mainThread.start()
    
lines = []
list_of_files = os.listdir()
for i in range(len(list_of_files)):
    df = pd.read_excel(list_of_files[i], skiprows=1)
    df.columns = [1, 2]
    region = df.iloc[0].loc[2]
    df = df.iloc[6:]
    for x in range (len(df)):
        line = [df.iloc[x].loc[1], df.iloc[x].loc[2], region]
        lines.append(line)
data = pd.DataFrame(lines, columns=[1, 2, 3])
data = data.drop_duplicates(subset=[1, 2, 3], keep='first')
data[1] = data[1].astype('str')
data[1] = data[1].apply(lambda a: a[6:10] + '-' + a[3:5] + '-' + a[:2])
data = data.reindex(columns = [1, 2, 3, 'dayofweek'])
data.columns = ['date', 'price_hour', 'region', 'dayofweek']
data['date'] = pd.to_datetime(data['date'])
data['dayofweek'] = data['date'].dt.dayofweek + 1
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
data.to_excel(writer, 'Sheet1')
writer.save()