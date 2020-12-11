# Step03 needs "cnt.pkl" generated in Step01.
# Step03 picks "Hot stocks" using the PD data downloaded from Yahoo.
# Step03 also pickles "Hot stocks" ticker list("ticker_list") into "ticker_list.pkl".
# Step03 then creates messages and tweets them.
print('==============================================')
print('            Step03 Started')
print('==============================================')
import pandas_datareader as pdr
from pandas import read_pickle, to_pickle
from datetime import date, timedelta
import tweet_func
from config import keys

# Load the Counter object generated in Step01
cnt = read_pickle('cnt.pkl')

# Generate top ranking and ticker list(input data for Yahoo)
temp = ''
ticker_list = []
for i_tuple in cnt:
    if i_tuple[1] >= 3:
        temp = temp + i_tuple[0]
        temp2 = i_tuple[0].replace(' ', '')
        temp2 = temp2[1:]
        ticker_list.append(temp2)
print(temp)

# Create "Hot stocks" msg
# Get data from Yahoo
today = date.today()
startday = today - timedelta(days=20)
pd_data = pdr.get_data_yahoo(ticker_list, startday, today)
# Create messages
ticker_list.clear()
tweet_list = []
row = 0
temp = 'Ticker Price Vol x10dAV\n'
line = '${0:4} {1:+6.1%} {2:+5.0%} {3:4.2f}\n'
for ticker in pd_data['Close'].columns:
    j = pd_data['Close'].pct_change()[ticker][-1]
    k = pd_data['Volume'].pct_change()[ticker][-1]
    l = pd_data['Volume'][ticker][-1]
    m = pd_data['Volume'].rolling(10).mean()[ticker][-2]
    n = l/m
    if j > 0 and k > 0 and n > 1.2:
        ticker_list.append(ticker)
        temp = temp + line.format(ticker, j, k, n)
        row = row + 1
        if row == 9:
            tweet_list.append(temp)
            temp = 'Ticker Price Vol x10dAV\n'
            row = 0
if row != 0:
    tweet_list.append(temp)
print('==============================================')

# Print and pickle ticker_list(input data of Step04)
print(ticker_list)
to_pickle(ticker_list, 'ticker_list.pkl')

# Tweet msgs
page = 1
for tweet in tweet_list:
    tweet = 'Hot stocks!\n' + tweet + '(' + str(page) + '/' +str(len(tweet_list)) + ')'
    page = page + 1
    print('==============================================')
    print(tweet)
    print('----------------------------------------------')
    print('word count =', len(tweet))
    tweet_func.tweet_msg(keys, tweet)
print('==============================================')
print('            Step03 Completed!')
print('==============================================')
