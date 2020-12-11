# is_holiday() determines if today is a holiday and ends with rc=255 if it is a holiday.
import pandas_datareader as pdr
from pandas import to_pickle, read_pickle
from datetime import date, timedelta, datetime
from sys import exit

def is_holiday(a=0):
    print('Now:', datetime.now())
    print('==============================================')
    today = date.today()
    # if a==0(default) get market data from Yahoo
    if a==0:
        startday = today - timedelta(days=20)
        df_AAPL = pdr.get_data_yahoo('AAPL', startday, today)
        to_pickle(df_AAPL, 'df_AAPL.pkl')
    # if a!=0 use pickled data
    else:
        df_AAPL = read_pickle('df_AAPL.pkl')
    lastdate = df_AAPL.index[-1]
    if str(today) != str(lastdate)[0:10]:
        print('Today is a holiday!')
        exit(255)
