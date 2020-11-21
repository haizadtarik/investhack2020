from bs4 import BeautifulSoup
from requests import get
import random 
import time
import pandas as pd
import re
import string  

# ============= FA ============
def get_fa(stock):
    headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    fa_url = 'https://www.investing.com/equities/'+stock+'-financial-summary'
    response = get(fa_url, headers=headers)
    print(response)
    html_soup = BeautifulSoup(response.text, 'html.parser')

# ============= TA ============
def get_ta(stock):
    headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    ta_url = 'https://www.investing.com/equities/'+stock+'-technical'
    response = get(ta_url, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    last_price = float(str(html_soup.find_all('span', id="fl_header_pair_lst")[0]).split(">")[1].strip('</span>'))
    ta = html_soup.find_all('div', class_="halfSizeColumn float_lang_base_1")
    rsi = float(str(ta[0].find_all('td', class_="right")[0]).split(">")[1].strip('</td>'))
    macd = float(str(ta[0].find_all('td', class_="right")[3]).split(">")[1].strip('</td>'))
    # ------ Moving averages -----
    ma = html_soup.find_all('div', class_="halfSizeColumn float_lang_base_2")
    ma10 = float(str(ma[0].find_all('td')[4]).split("<br/>")[0].strip('<td>\n\t')) 
    ema10 = float(str(ma[0].find_all('td')[5]).split("<br/>")[0].strip('<td>\n\t')) 
    ma20 = float(str(ma[0].find_all('td')[7]).split("<br/>")[0].strip('<td>\n\t')) 
    ema20 = float(str(ma[0].find_all('td')[8]).split("<br/>")[0].strip('<td>\n\t')) 
    ma50 = float(str(ma[0].find_all('td')[10]).split("<br/>")[0].strip('<td>\n\t')) 
    ema50 = float(str(ma[0].find_all('td')[11]).split("<br/>")[0].strip('<td>\n\t')) 
    ma100 = float(str(ma[0].find_all('td')[13]).split("<br/>")[0].strip('<td>\n\t')) 
    ema100 = float(str(ma[0].find_all('td')[14]).split("<br/>")[0].strip('<td>\n\t'))
    ma200 = float(str(ma[0].find_all('td')[16]).split("<br/>")[0].strip('<td>\n\t')) 
    ema200 = float(str(ma[0].find_all('td')[17]).split("<br/>")[0].strip('<td>\n\t')) 
    data = {'rsi': rsi,
            'macd': macd,
            'ma10': ma10,
            'ema10': ema10,
            'ma20': ma20,
            'ema20': ema20,
            'ma50': ma50,
            'ema50': ema50,
            'ma100': ma100,
            'ema100': ema100,
            'ma200': ma200,
            'ema200': ema200
    }
    return data




