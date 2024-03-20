from bs4 import BeautifulSoup as bs
import os, requests, threading
import time as t
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Firefox(executable_path=r'C:/Users/playmen/source/python/mosreg/geckodriver.exe', options=options)
links = []
for i in range(1, 80):
    driver.get('https://ktc.mosreg.ru/dokumenty?page=' + str(i))
    soup2 = bs(driver.page_source, "html.parser")
    x = 0
    while x != -1:
        if str(soup2)[str(soup2).find('"doc-block__date"', x) + 26: str(soup2).find('"doc-block__date"', x) + 28] == '23':
            x = str(soup2).find('"doc-block__date"', x + 1)
            if str(soup2)[str(soup2).find('</svg>' , x) + 6 : str(soup2).find('<', str(soup2).find('</svg>', x) + 6)].find('Об установлении тарифов в сфере теплоснабжения') != -1:
                links.append(str(soup2)[str(soup2).find('http', x) : str(soup2).find('"', str(soup2).find('http', x))])
        else:
            x = str(soup2).find('"doc-block__date"', x + 1)
    print(i)
driver.close()

download_dir = r'C:\Users\playmen\source\python\mosreg\data'
names = []

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.headless = True
options.add_argument("--window-size=1920,1080")

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", download_dir)
profile.set_preference("browser.helperApps.neverAsk.openFile", "application/octet-stream")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
profile.set_preference("pdfjs.disabled", True);

driver = webdriver.Firefox(executable_path=r'C:/Users/playmen/source/python/mosreg/geckodriver.exe', options=options, firefox_profile=profile)

def callback():
    TimeList = []
    for i in os.listdir(download_dir):
        TimeList.append(os.path.getmtime(download_dir + "\\" + i))
    TimeList.sort()
    for i in range(len(names)):
        for x in os.listdir(download_dir):
            if os.path.getmtime(download_dir + "\\" + x) == TimeList[i]:
                os.rename(download_dir + "\\" + x, download_dir + "\\" + names[i])
                print(names[i])
                break
                
for i in links:
    driver.get(i)
    soup = bs(driver.page_source, "html.parser")
    if str(soup).find('№', str(soup).find('page__title page__title--small'), str(soup).find('page__title page__title--small') + 150) != -1:
        name = str(soup)[str(soup).find('№', str(soup).find('page__title page__title--small')) - 11 : str(soup).find('<' , str(soup).find('№', str(soup).find('page__title page__title--small')) - 11)]
    else:
        name = str(soup)[str(soup).find('>', str(soup).find('page__title page__title--small')) + 1 : str(soup).find('<' , str(soup).find('>', str(soup).find('page__title page__title--small')) + 1)]
    name = name.replace('"', "'").replace("'\'", '').replace('/', '').replace(':', '').replace('|', '').replace('*', '').replace('\r', '').replace('\n', '')
    while name.count('') > 187:
        name = name[:-1]
    name = name + '.pdf'
    if name[:1] != 'П':
        names.append(name)
        print(name)
        driver.find_element_by_xpath("//a[@class='doc-label doc-label--link list-bar__item']").click()
driver.close()
print('part2')
timer = threading.Timer(5.0, callback)
timer.start()

TimeList = []
for i in os.listdir(download_dir):
    TimeList.append(os.path.getmtime(download_dir + "\\" + i))
TimeList.sort()
for i in range(len(names)):
    for x in os.listdir(download_dir):
        if os.path.getmtime(download_dir + "\\" + x) == TimeList[i]:
            os.rename(download_dir + "\\" + x, download_dir + "\\" + names[i])
            print()
            break