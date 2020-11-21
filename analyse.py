from bs4 import BeautifulSoup
from requests import get
import random 
import time
import pandas as pd
import re
import string  

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

# ============= FA ============
def get_fa(stock):
    fa_url = 'https://www.investing.com/equities/'+stock
    response = get(fa_url, headers=headers)
    print(response)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    overview = html_soup.find_all('div', class_="clear overviewDataTable overviewDataTableWithTooltip")[0].find_all('span', class_="float_lang_base_1")
    values = html_soup.find_all('div', class_="clear overviewDataTable overviewDataTableWithTooltip")[0].find_all('span', class_="float_lang_base_2 bold")
    range_52 = str(values[4]).split(">")[1].strip('</span>')
    market_cap = str(values[7]).split(">")[1].strip('</span>')
    PE_ratio = str(values[10]).split(">")[1].strip('</span>')
    Share_outstanding = str(values[13]).split(">")[1].strip('</span>')
    revenue = str(values[2]).split(">")[1].strip('</span>')
    EPS = str(values[5]).split(">")[1].strip('</span>')
    dividend_yield = str(values[8]).split(">")[1].strip('</span>')
    next_earning_date = str(values[14]).split(">")[2].strip('</span>')

    fa_url = 'https://www.investing.com/equities/'+stock+'-financial-summary'
    response = get(fa_url, headers=headers)
    print(response)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    table = str(html_soup.find_all('table', class_="genTbl openTbl companyFinancialSummaryTbl")[1])
    asset = table.split('<tr>')[2].split('<td>')[1].split('</td>')[0]
    liabilities = table.split('<tr>')[3].split('<td>')[1].split('</td>')[0]
    data = {  
        'range_52': range_52, 
        'market_cap': market_cap, 
        'PE_ratio': PE_ratio, 
        'Share_outstanding': Share_outstanding, 
        'revenue': revenue, 
        'EPS': EPS, 
        'dividend_yield': dividend_yield, 
        'next_earning_date': next_earning_date,
        'asset': asset,
        'liabilities': liabilities
    }
    return '\n'.join([f'{key}: {value}' for key, value in data.items()])

# ============= TA ============
def get_ta(stock):
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
    data = {'last_price': last_price,
            'rsi': rsi,
            'macd': macd,
            # 'ma10': ma10,
            # 'ema10': ema10,
            'ma20': ma20,
            'ema20': ema20,
            'ma50': ma50,
            'ema50': ema50,
            # 'ma100': ma100,
            # 'ema100': ema100,
            'ma200': ma200,
            'ema200': ema200
    }
    return '\n'.join([f'{key}: {value}' for key, value in data.items()])

def get_news(stock):
    fa_url = 'https://www.investing.com/equities/'+stock+'-news'
    response = get(fa_url, headers=headers)
    print(response)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    news = html_soup.find_all('div', class_="mediumTitle1")[1].find_all('article', class_='js-article-item articleItem') 
    if len(news) > 2:
        news1_url = str(news[0].find_all('a')[1]).split('>')[0].split(' ')[2].strip('href="')
        news1 = ' '.join(str(news[0].find_all('a')[1]).split('>')[0].split(' ')[3:]).strip('title="')
        news2_url = str(news[1].find_all('a')[1]).split('>')[0].split(' ')[2].strip('href="')
        news2 = ' '.join(str(news[1].find_all('a')[1]).split('>')[0].split(' ')[3:]).strip('title="')
        news3_url = str(news[2].find_all('a')[1]).split('>')[0].split(' ')[2].strip('href="')
        news3 = ' '.join(str(news[2].find_all('a')[1]).split('>')[0].split(' ')[3:]).strip('title="')
        data = {
            news1: news1_url,
            news2: news2_url,
            news3: news3_url
        }
    elif len(news) == 2: 
        news1_url = str(news[0].find_all('a')[1]).split('>')[0].split(' ')[2].strip('href="')
        news1 = ' '.join(str(news[0].find_all('a')[1]).split('>')[0].split(' ')[3:]).strip('title="')
        news2_url = str(news[1].find_all('a')[1]).split('>')[0].split(' ')[2].strip('href="')
        news2 = ' '.join(str(news[1].find_all('a')[1]).split('>')[0].split(' ')[3:]).strip('title="')
        data = {
            news1: news1_url,
            news2: news2_url
        }
    elif len(news) == 1:
        news1_url = str(news[0].find_all('a')[1]).split('>')[0].split(' ')[2].strip('href="')
        news1 = ' '.join(str(news[0].find_all('a')[1]).split('>')[0].split(' ')[3:]).strip('title="')
        data = {
            news1: news1_url
        }
    else: 
        data = {
            'now news': ' '
        }
    return '\n\n'.join([f'{key} \nhttps://www.investing.com{value}' for key, value in data.items()])