import json
from pprint import pprint
from urllib.parse import urlencode

import numpy as np
import pandas as pd
import requests
from nsepython import nse_optionchain_scrapper
from nsetools import Nse
from selenium import webdriver
import os
nse = Nse()
print(nse)


def get_session_cookies():
    link = "https://www.nseindia.com"
    driver = webdriver.Chrome()
    driver.get(link)
    #current_dir = '/Users/A119619981/Documents/Shikha/t-systems/Personal space/PY/chromedriver.exe'
    #driver = webdriver.Chrome()
    #driver.get("https://www.nseindia.com")
    cookies = driver.get_cookies()
    cookies_dict = {}
    with open('cookies', 'w') as line:
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        line.write(json.dumps(cookies_dict))
    driver.quit()
    return cookies_dict


def get_option_chain_data(symbol, instrument, date_="-"):
    base_url = "https://www.nseindia.com/api/option-chain-indices?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    }
    parameters = {
        "segmentLink": 17,
        "instrument": instrument,
        "symbol": symbol,
        "date": date_
    }
    url = base_url + urlencode(parameters)
    print(url)
    try:
        cookie_dict = json.loads(open('cookies').read())
    except Exception as e:
        print('exception while reading{}', e)
        cookie_dict = get_session_cookies()

    session = requests.session()

    for cookie in cookie_dict:
        if cookie == "bm_sv":
            session.cookies.set(cookie, cookie_dict[cookie])
    try:
        r = session.get(url, headers=headers).json()
        df = pd.DataFrame(r)
        pprint(df['Strike Price'])
    except Exception as e:
        pprint("Exception while reading from session")
        cookie_dict = get_session_cookies()
        for cookie in cookie_dict:
            if cookie =="bm_sv":
                session.cookies.set(cookie, cookie_dict[cookie])

        r = session.get(url, headers=headers).json()
        df = pd.DataFrame(r)
        pprint(df['Strike Price'])

        # df.columns = ["CE Chart", "CE OI", "CE Change in OI", "CE Volume", "CE IV", "CE LTP", "CE Net Change", "CE Bid Qty",
        #           "CE Bid Price", "CE Ask Price", "CE Ask Quantity",
        #           "Strike Price",
        #           "PE Bid Qty", "PE Bid Price", "PE Ask Price", "PE Ask Qty", "PE Net Change", "PE LTP", "PE IV",
        #           "PE Volume", "PE Change in OI", "PE OI", "PE Chart"]
    return df

get_option_chain_data("BANKNIFTY", "OPTSTK")
#nse_optionchain_scrapper("NIFTY")