'''
Scrape Google News using bs4
'''
from requests import get
# from contextlib import closing
from bs4 import BeautifulSoup
import requests
from lxml import html
import pandas as pd
import time
import datetime as datetime
import random

timelist = pd.read_csv('techindicators_20.csv')['Date'][:]
Ticker = 'Microsoft Stock News'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
to_merge = pd.DataFrame({'Date': [],'Ticker': [], 'Url':[], 'headline': [], 'source': [], 'snippet': []})
it = 0
for date in timelist:
    it += 1
    #if it%100 != 0:
    #print('Fetching ',timelist[it])

    time.sleep(abs(random.gauss(0,2)))

    # Create URL
    Date = str(date).replace("-","")
    URL = 'https://www.google.com/search?q='+Ticker+'+'+Date+'&source=lnms&tbm=nws'

    # Get URL
    raw_html = requests.get(URL, headers=headers)
    soup = BeautifulSoup(raw_html.text, 'lxml')
    #title_list = soup.find_all("a", class_="l lLrAF")
    title_list = soup.find_all("a", class_="WlydOe")

    #date_list = soup.find_all("span", class_="f nsa fwzPFf")
    date_list = soup.find_all("div", class_="OSrXXb ZE0LJd YsWzw")

    #ource_list = soup.find_all("span", class_="xQ82C e8fRJf")
    source_list = soup.find_all("div", class_="CEMjEf NUnG9d")

    #snippet_list = soup.find_all("div", class_="st")
    snippet_list = soup.find_all("div", class_="GI74Re nDgy9d")

    #print(len(title_list), len(date_list), len(source_list), len(snippet_list))
    # Parse elements
    t_list = soup.find_all("div", class_="mCBkyc ynAwRc MBeuO nDgy9d")
    title = []
    date = []
    source = []
    snippet = []
    url = []

    for elem in t_list:
        valid = str(elem).split('>')[1][:-5]
        #if it == 1:
        #    print(valid)
        title.append(valid)

    for elem in title_list:
        valid = str(elem).replace("<em>", "").replace("</em>", "")[19:-4]
        out1 = valid.split("=")[2][1:-6]
        out2 = valid.split("=")[3]
        url.append(out1)
        #title.append(out2)
        #if it == 1:
        #    print(valid)

    for elem in date_list:
        valid = str(elem).split('>')[2][:-6]
        date.append(valid)
        #if it == 1:
            #print(valid)

    for elem in source_list:
        valid = str(elem).split('>')[-3][:-6]
        source.append(valid)
        #if it == 1:
        #    print(valid)

    for elem in snippet_list:
        valid = str(elem).replace("<em>", "").replace("</em>", "")[:-6].split('>')[1]
        snippet.append(valid)
        #if it == 1:
        #    print(valid)

    if len(title) == len(date) and len(title) == len(url) and len(title) == len(source) and len(title) == len(snippet):
        ticker = ['MSFT']*len(title)
        news = pd.DataFrame({'Date':date,'Ticker': ticker,'Url': url, 'headline':title, 'source': source, 'snippet': snippet})
        to_merge = pd.concat([to_merge,news])

to_merge.to_csv('MSFT_news.csv')
