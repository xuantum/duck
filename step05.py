# Step05 needs "pd_data.pkl" generated in Step04.
# Step05 analyzes the charts generated from the PD data pickled in Step04.
# Step05 saves the tickers into "temp_list" if the chart is in good shape.
# Comparing with the history, if the tickers listed in "temp_list" had been tweeted within the recent 5 days, 
# Step05 eliminates them and makes the final ticker list("ticker_list").
# Step05 then generates chart images of tickers listed in "ticker_list" and tweets them.
print('==============================================')
print('            Step05 Started')
print('==============================================')
# Change directry
#import os
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import mplfinance as mpf
from numpy import nanmax, nanmin
from datetime import date, timedelta, datetime
import tweet_func
from config import keys

# Load the PD object generated in Step04
df = pd.read_pickle('pd_data.pkl')
# Create temp df
df_pctchg_close = df['Close'].pct_change()
# Normalize df['Close']
f = lambda x: (x - nanmin(x)) / (nanmax(x) - nanmin(x))
df_norm_close = df['Close'].apply(f)

# Analyze the charts and pick the tickers for tweeting saving them into "temp_list"
print('==============================================')
print('ticker, recent_high, today_price, ratio, norm_today_price, max_chg, min_chg')
line = '${0:4} {1:7.2f} {2:7.2f} {3:4.2f} {4:4.2f} {5:+6.1%} {6:+6.1%}'
temp_list = []
for ticker in df['High'].columns:
    max_high = nanmax(df['High'][ticker][:-1].values)
    min_close = nanmin(df['Close'][ticker].values)
    recent_high = nanmax(df['High'][ticker][-21:-1].values)
    today_price = df['Close'][ticker][-1]
    ratio = (today_price - min_close) / (max_high - min_close)
    norm_today_price = df_norm_close[ticker][-1]
    max_chg = nanmax(df_pctchg_close[ticker][-20:].values)
    min_chg = nanmin(df_pctchg_close[ticker][-20:].values)
    # Extraction condition(your strategy!)
    if today_price>=max_high:
        # Save the extracted tickers into "temp_list"
        temp_list.append(ticker)
        print(line.format(ticker, recent_high, today_price, ratio, norm_today_price, max_chg, min_chg))

# Compare with history and generate final ticker list("ticker_list") for tweeting
# Read history file
with open('tweet_history.txt', encoding='utf-8') as f:
    history = f.readlines()
# Compare with the history and eliminate tickers that were tweeted within recent 5 days
ticker_list = []
today = date.today()
before_day = today - timedelta(days=5)
for ticker in temp_list:
    flag = 0
    for i_str in history:
        # Generate date-type from the record in the history
        recorded_day = datetime.strptime(i_str[:10], "%Y-%m-%d").date()
        # If the record is old(more than 5 days) then read next record
        if recorded_day < before_day:
            continue
        # If the record is not old(within 5 days) then extract a ticker from the record
        i_str = i_str[11:].replace('\n', '')
        # If the tickers are same, that means the ticker in "temp_list" was tweeted within recent 5 days
        if ticker == i_str:
            flag = flag + 1
            break
    # If the ticker was not tweeted within recent 5 days, add the ticker into "ticker_list"
    if flag == 0:
        ticker_list.append(ticker)

# Tweet messages about stocks listed in "ticker_list" and update the history
for ticker in ticker_list:
    print('==============================================')
    # Create a message
    tweet = '$' + ticker + ' is likely to break!\n(Daily chart)'
    print(tweet)
    print('----------------------------------------------')
    # Generate a chart image
    df_chart = df.xs(ticker, level='Symbols', axis=1)
    file_path = './images/' + ticker + '.png'
    mpf.plot(df_chart, type='candle', volume=True, mav=(5), figratio=(16,9), savefig=file_path)
    # Tweet a message with a image
    tweet_func.tweet_msg(keys, tweet, file_path)
    # Update the history file
    with open('tweet_history.txt','a', encoding='utf-8') as f_out:
        f_out.write(str(today) + ' ' + ticker + '\n')
print('==============================================')
print('            Step05 Completed!')
print('==============================================')
