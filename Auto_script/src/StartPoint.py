# get current strick price
# divide /100 as there is a gap of 100 in strick price
# to buy CE add 300 in current sp
# high of sp CE's till 10 AM
# if high breaks buy CE
# to buy PE subtract 300 from current sp
# high of sp PE's till 10 AM
# if high breaks buy PE
# ** live data needs to be fetched form alicis or zerodha
import pandas as pd
from nsepython import *
from nsetools import Nse
from datetime import datetime, time

nse = Nse()


def get_nse_quote_meta(symbol, strike_price, option_type, expiry):
    return nse_quote_meta(symbol, optionType=option_type, strikePrice=strike_price)


def get_option_chain_ltp(symbol, strike_price, option_type, expiry):
    return nse_quote_ltp(symbol, optionType=option_type, strikePrice=strike_price)


def get_current_sp(symbol):
    # get the ltp for symbol
    ltp = nse_quote_ltp(symbol)
    print(ltp)
    rf_ltp = round(ltp / 100) * 100
    print(rf_ltp)
    ce_to_buy = rf_ltp + 300
    pe_to_buy = rf_ltp - 300

    # get ce's current price & day high
    ce_cp = get_option_chain_ltp(symbol, ce_to_buy, "CE", 0)
    print(ce_to_buy, "ce current price is :{} ", ce_cp)

    # get pe's current price & day high
    pe_cp = get_option_chain_ltp(symbol, pe_to_buy, "PE", 0)
    print(pe_to_buy, "pe current price is :{} ", pe_cp)

    q = nse.get_index_quote('BANKNIFTY2142231800PE')
    print(q)


# get_current_sp('BANKNIFTY')

#----------------
# get 300+ CE option
def get_ce_option(round_price):
    ce_to_buy = (round(round_price / 100) * 100) + 300
    ce_cp = get_option_chain_ltp('BANKNIFTY', ce_to_buy, "CE", 0)
    print(ce_to_buy, "ce current price is :{} ", ce_cp)
    print("meta data")
    meta_data = nse_quote_meta("BANKNIFTY","latest","CE",ce_to_buy)
    print(meta_data)

    if is_time_between(time(9, 30), time(23, 5)):
        highPrice = meta_data['highPrice']
        print("highPrice till 10:05AM is ", highPrice)



# get 300- PE option
def get_pe_option(round_price):
    pe_to_buy = (round(round_price / 100) * 100) - 300
    pe_cp = get_option_chain_ltp('BANKNIFTY', pe_to_buy, "PE", 0)
    print(pe_to_buy, "pe current price is :{} ", pe_cp)


# check/load day high low @ 10.05
def load_low_high():
    # fetch from api
    nifty_bank_info = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK')
    bankNifty_day_high = nifty_bank_info['data'][0]['dayHigh']
    bankNifty_day_low = nifty_bank_info['data'][0]['dayLow']
    return bankNifty_day_high, bankNifty_day_low


# time check @10.05
def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


# IF CURRENT TIME IS MORE THAN 10:05 DON'T CHECK THE HIGH LOW USE THE STORED ONE
def fetch_nse(bank_nifty_day_high, bank_nifty_day_low):
    # set high low @ 10.5
    if is_time_between(time(9, 30), time(23, 5)):
        bank_nifty_day_high, bank_nifty_day_low = load_low_high()
        print(bank_nifty_day_high, bank_nifty_day_low)
    else:
        print("fetched high low till 10.5 only",bank_nifty_day_high, bank_nifty_day_low)

    # while(1):
    # fetch from api
    nifty_bank_info = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK')
    bank_nifty_current_price = nifty_bank_info['data'][0]['lastPrice']
    bank_nifty_current_price = 39609

    if bank_nifty_current_price > bank_nifty_day_high:
        print('high broken')
        # get ce data
        get_ce_option(bank_nifty_current_price)
    elif bank_nifty_current_price < bank_nifty_day_low:
        print('low broken')
        # get pe data
        get_pe_option(bank_nifty_current_price)
    elif bank_nifty_day_low < bank_nifty_current_price < bank_nifty_day_high:
        print('side wise')



def fetch_bank_nifty_high_low():
    nifty_bank_info = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK')
    bank_nifty_current_option = nifty_bank_info['data'][0]['lastPrice']
    print("bank nifty current strik price is ", bank_nifty_current_option)
    bank_nifty_day_high = nifty_bank_info['data'][0]['dayHigh']
    bank_nifty_day_low = nifty_bank_info['data'][0]['dayLow']
    return bank_nifty_day_high, bank_nifty_day_low


# 1 time run to
# fetch high low of banknifty @ 10.04 &
# decide which ce pe to watch
# then fetch ce pe high
#fetch_init()
