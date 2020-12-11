# Step04 needs "ticker_list.pkl" generated in Step03.
# Step04 downloads half-year PD data of stocks that were picked in Step03, using pandas_datareader.
# Step04 then pickles the PD data into "pd_data.pkl".
print('==============================================')
print('            Step04 Started')
print('==============================================')
import pandas_datareader as pdr
from time import sleep
from pandas import to_pickle, read_pickle
from datetime import date, timedelta

# Load ticker_list generated in Step03
ticker_list = read_pickle('ticker_list.pkl')
print(ticker_list)

# Get half-year data from Yahoo
today = date.today()
startday = today - timedelta(days=183)
pd_data = pdr.get_data_yahoo(ticker_list, startday, today)

# Pickle the pd object(input data of Step05)
to_pickle(pd_data, 'pd_data.pkl')
sleep(1)
print('==============================================')
print('            Step04 Completed!')
print('==============================================')
