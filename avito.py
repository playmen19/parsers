from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time as t
import os
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_

data = []
url = 'https://www.avito.ru/moskva_i_mo/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?f=ASgBAQECAkSUA9AQ5usOAgFA2Ag0ylnQWc5ZAkWSCBZ7ImZyb20iOjEzMCwidG8iOm51bGx9xpoMH3siZnJvbSI6MTcwMDAwMDAsInRvIjoyNTAwMDAwMH0&s=104'
find = url
headers = {'authority': 'www.avito.ru',
           'method': 'GET',
           'path': '/',
           'scheme': 'https',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'ru,en;q=0.9',
           'cache-control': 'no-cache',
           'pragma': 'no-cache',
           'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'same-origin',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.765 Yowser/2.5 Safari/537.36'
          }

cookies = {'buyer_laas_location' : '637640',
           'luri' : 'moskva',
           'buyer_location_id' : '637640',
           'abp' : '1',
           'SEARCH_HISTORY_IDS' : '4'
          }

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

s = requests.Session()
s.headers = headers
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
s.mount('https://', adapter)

for i in range(10):
    try:
        soup = bs(s.get(find, cookies = cookies, verify = 'cert.pem', timeout=5).text, "html.parser")
        break
    except:
        timeSoup = t.time()
        print(t.strftime('%H:%M:%S', t.gmtime(int(str(timeSoup)[: str(timeSoup).find('.', 0)]) + 10800)) + ' Request failed! Probably internet problems.')

links = []
allA = soup.find_all('a', itemprop="url")
for i in allA:
    links.append(i["href"])

allSpan = soup.find_all('span', class_="styles-module-text-InivV")
page = []
for i in allSpan:
    page.append(i.text)
print(page[-1])

for i in range(2, int(page[-1]) - 19):
    t.sleep(3)
    print(str(i) + ' Страница')
    find = url + '&p=' + str(i)
    soup = bs(s.get(find, verify = 'cert.pem').text, "html.parser")
    allA = soup.find_all('a', itemprop="url") 
    for i in allA:
        links.append(i["href"])

links = list(dict.fromkeys(links))
print(len(links))

for x in range(len(links)):
    find = 'https://www.avito.ru' + links[x]
    t.sleep(3)
    for i in range(10):
        try:
            soup = bs(s.get(find, cookies = cookies, verify = 'cert.pem').text, "html.parser")
            break
        except:
            timeSoup = t.time()
            print(t.strftime('%H:%M:%S', t.gmtime(int(str(timeSoup)[: str(timeSoup).find('.', 0)]) + 10800)) + ' Request failed! Probably internet problems.')

    allDiv = []
    allDiv = soup.find_all('div', itemprop="description")
    if allDiv != []:
        for i in allDiv:
            text = i.text
        if text.find('семейный') != -1 or text.find('Семейный') != -1 or text.find('семейную') != -1 or text.find('Семейную') != -1 or text.find('семейной') != -1 or text.find('Семейной') != -1 or text.find('семейная') != -1 or text.find('Семейная') != -1 or text.find('семейные') != -1 or text.find('Семейные') != -1 or text.find('семейными') != -1 or text.find('Семейными') != -1 or text.find('льготный') != -1 or text.find('Льготный') != -1 or text.find('льготную') != -1 or text.find('Льготную') != -1 or text.find('льготной') != -1 or text.find('Льготной') != -1 or text.find('льготная') != -1 or text.find('Льготная') != -1 or text.find('льготные') != -1 or text.find('Льготные') != -1 or text.find('льготными') != -1 or text.find('Льготными') != -1:
            data.append(find)
            print(find)
        print(x)
    else:
        print('ERROR')

df = pd.DataFrame(data, columns = [0]).reset_index(drop=True)
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1')
writer.close()