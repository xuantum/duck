# duck
This Python program is a Twitter bot that automatically analyzes the stock market and tweets analysis results and chart images. It has three functions. The first is to collect tweets tweeted by stock market influencers and create a WordCloud image. The second is to download stock data using pandas-datareader and create "Hot stocks" list. The third is to analyze stock charts and determine if it is in good shape. All of these functions are processed and tweeted automatically.

## Requirement
Python3  
Twitter API keys  

## Python requirements.txt
>requests==2.25.0  
>numpy==1.19.4  
>matplotlib==3.3.3  
>pandas==1.1.4  
>mplfinance==0.12.7a0  
>wordcloud==1.8.1  
>requests_oauthlib==1.3.0  
>pandas_datareader==0.9.0  

## Setup
mkdir "data" and "images".  
Rewrite Twitter API keys in "config.py".  
Add users that you want to watch to "all_userlist.txt".  
Place "tweet_history.txt" as empty.  

## Usage
python step01.py  
python step02.py  
python step03.py  
python step04.py  
python step05.py  

## Description of each step
### Step01
Step01 uses the Twitter API to collect tweets and save them in "./data/xxxx_data.txt".  
Step01 then extracts ticker symbols into a text object and pickles the object into "tokenized_text.pkl".  
Step01 also creates a Counter object and pickles the object into "cnt.pkl".  
### Step02
Step02 needs "tokenized_text.pkl" and "cnt.pkl" generated in Step01.  
Step02 creates a "Top tweeted stocks" message and a wordcloud image and tweets them.  
### Step03
Step03 needs "cnt.pkl" generated in Step01.  
Step03 picks "Hot stocks" using the PD data downloaded from Yahoo.  
Step03 also pickles "Hot stocks" ticker list("ticker_list") into "ticker_list.pkl".  
Step03 then creates messages and tweets them.  
### Step04
Step04 needs "ticker_list.pkl" generated in Step03.  
Step04 downloads half-year PD data of stocks that were picked in Step03, using pandas_datareader.  
Step04 then pickles the PD data into "pd_data.pkl".  
### Step05
Step05 needs "pd_data.pkl" generated in Step04.  
Step05 analyzes the charts generated from the PD data pickled in Step04.  
Step05 saves the tickers into "temp_list" if the chart is in good shape.  
Comparing with the history, if the tickers listed in "temp_list" had been tweeted within the recent 5 days, Step05 eliminates them and makes the final ticker list("ticker_list").  
Step05 then generates chart images of tickers listed in "ticker_list" and tweets them.  

## Maintenance
When the history file grows larger, clear the contents.

## License
This software is released under [the MIT License](https://opensource.org/licenses/mit-license.php)

## Author
[xuantum](https://github.com/xuantum)
