from src.kite_trade import *


# # Second way is provide 'enctoken' manually from 'kite.zerodha.com' website
# # Than you can use login window of 'kite.zerodha.com' website Just don't logout from that window
# # # Process shared on YouTube 'TradeViaPython'

enctoken = "MJiJt6EKbrVd7a2JWZlOyop+5rQXBYWMZOBz4t/XmIlMJLct8o0xcuzXgihYE0mjFn9VH4TYfGe7lQpoewNZI7bO7BJg6NAUe+HSoftoqp6zyp+QpyCPmA=="
kite = KiteApp(enctoken=enctoken)
print(kite.quote(["NFO:BANKNIFTY22SEPFUT"]))
