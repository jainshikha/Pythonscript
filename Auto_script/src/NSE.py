from nsepython import *


def get_meta_data(option_type, strike_price):
    print("strike_price is ", strike_price, option_type, "at", option_type, "side")
    meta_data = nse_quote_meta("BANKNIFTY", "latest", option_type, strike_price)
    high_price = meta_data['highPrice']
    return high_price


# get 300+ CE option
def get_ce_option(day_high):
    print((round(day_high / 100) * 100))
    ce_to_buy = (round(day_high / 100) * 100) + 300
    high_price = get_meta_data("CE", ce_to_buy)
    print("highPrice till 10:05AM is ", high_price)
    return high_price, ce_to_buy, "CE"


# get 300- PE option
def get_pe_option(day_low):
    print((round(day_low / 100) * 100))
    pe_to_buy = (round(day_low / 100) * 100) - 300
    high_price = get_meta_data("PE", pe_to_buy)
    print("highPrice till 10:05AM is ", high_price)
    return high_price, pe_to_buy, "PE"


def fetch_bank_nifty_high_low():
    nifty_bank_info = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK')
    bank_nifty_current_option = nifty_bank_info['data'][0]['lastPrice']
    print("bank nifty current strik price is ", bank_nifty_current_option)
    # bank_nifty_day_high = nifty_bank_info['data'][0]['dayHigh']
    # bank_nifty_day_low = nifty_bank_info['data'][0]['dayLow']
    return bank_nifty_current_option


ce_high = 0
ce_strike = 0
option_type_ce = 0
pe_high = 0
pe_strike = 0
option_type_pe = 0


def fetch_init():
    global ce_high
    global ce_strike
    global option_type_ce
    global pe_high
    global pe_strike
    global option_type_pe
    # fetch high low of banknifty @ 10.04 &
    bank_nifty_current_option = fetch_bank_nifty_high_low()
    # decide which ce pe to watch and then fetch ce & pe high
    ce_high, ce_strike, option_type_ce = get_ce_option(bank_nifty_current_option)
    pe_high, pe_strike, option_type_pe = get_pe_option(bank_nifty_current_option)
    print("ce high till 10:04 ", ce_high, "for strike ", ce_strike, option_type_ce)
    print("pe high till 10:04 ", pe_high, "for strike ", pe_strike, option_type_pe)


# 1 time run
# fetch high low of bank nifty @ 10.04 &
# decide which ce pe to watch and then fetch ce & pe high
fetch_init()


def get_option_chain_ltp(symbol, strike_price, option_type, expiry):
    return nse_quote_ltp(symbol, optionType=option_type, strikePrice=strike_price)


ce_purchase = None
pe_purchase = None


# stop loss 30%
def set_stop_loss(purchase_price):
    return purchase_price - (purchase_price * 0.3)


# target 50% then trail
def set_targe_and_trail(purchase_price):
    target_price = purchase_price + (purchase_price * 1)
    return purchase_price + (purchase_price * 1)


# repeat
# run in loop to check ltp of ce & pe to break the high
def check_for_high_break():
    ce_current = get_option_chain_ltp('BANKNIFTY', ce_strike, "CE", 0)
    print("CE current price is :{} ", ce_current)

    pe_current = get_option_chain_ltp('BANKNIFTY', pe_strike, "PE", 0)
    print("PE current price is :{} ", pe_current)
    pe_current = 240
    global ce_purchase, pe_purchase
    global sl
    if ce_purchase is None or pe_purchase is None:
        # if ce high breaks purchase ce
        if ce_current > ce_high:
            ce_purchase = ce_current
            sl = set_stop_loss(ce_purchase)
            print('high broken')
            print("purchase ce at ", ce_purchase)
            print('SL is ', sl)
            return ce_purchase, sl
        # elif pe high breaks purchase pe
        elif pe_current > pe_high:
            pe_purchase = pe_current
            sl = set_stop_loss(pe_purchase)
            print('high broken')
            print("purchase pe at ", pe_purchase)
            print('SL is ', sl)
            return pe_purchase, sl

    print(sl, pe_purchase, ce_purchase)
    # if current is sl hege with opposite option
    # if pe_current == sl and ce_current == sl:
    # trailing on 50% target 100%


# runs every 1 min
# run in loop to check ltp of ce & pe to break the high
# stop loss 30%
# trailing on 50%
# target 100%
purchase_price = None
sl = None
purchase_price, sl = check_for_high_break()
