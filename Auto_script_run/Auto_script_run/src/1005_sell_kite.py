from src.kite_trade import *
import pandas as pd

# # Second way is provide 'enctoken' manually from 'kite.zerodha.com' website
# # Than you can use login window of 'kite.zerodha.com' website Just don't logout from that window
# # # Process shared on YouTube 'TradeViaPython'

enctoken = "eSCUgMscug7MlNjnILhsc+UnF15immKdaX0JXh99KdoxYH3GMiXoz/x2TpT2D5LPwJfRlCUF+MC/CETROlkSUqwL+g+ajQ26X4jgGo1Q0zWKT46raVkjug=="
kite = KiteApp(enctoken=enctoken)
data = kite.quote("NFO:BANKNIFTY22SEPFUT")

print(data["NFO:BANKNIFTY22SEPFUT"])

print(data["NFO:BANKNIFTY22SEPFUT"]["last_price"])
# Get Historical Data
import datetime
instrument_token = 9604098
from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)     # From last & days
to_datetime = datetime.datetime.now()
interval = "5minute"
data2 = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
data1=pd.DataFrame(data2)
print(data1)
