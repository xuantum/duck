# Step01 uses the Twitter API to collect tweets and save them in "./data/xxxx_data.txt".
# Step01 then extracts ticker symbols into a text object and pickles the object into "tokenized_text.pkl".
# Step01 also creates a Counter object and pickles the object into "cnt.pkl".
print('==============================================')
print('            Step01 Started')
print('==============================================')
# Cahnge directory
#import os
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json
from pandas import to_pickle
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta, timezone, date, time
from time import sleep
from collections import Counter
import extract_func, holiday_func
from config import keys

# Get tweets of user_type. You can set how many days ago and from what time to get the data.
def getweet(user_type='all', since_day=1, since_time=17):
    # Twitter API URL
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    # Define timezones
    UTC = timezone.utc
    #JST = timezone(timedelta(hours=+9), 'JST')
    EDT = timezone(timedelta(hours=-4), 'EDT')
    #EST = timezone(timedelta(hours=-5), 'EST')

    # Create since_id
    today = date.today()
    yesterday = today - timedelta(days=since_day)
    since_date_time = datetime.combine(yesterday, time(since_time, 00), tzinfo=EDT)
    # UNIX time(msec)
    timestamp = int((since_date_time.astimezone(UTC) - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds()) * 1000 - 1288834974657
    # 22bit shift
    since_id = timestamp << 22
    print('Since:', since_date_time)
    print('----------------------------------------------')

    # Read user-list
    with open(user_type + '_userlist.txt', "r") as f_in:
        user_list = [v.rstrip() for v in f_in.readlines()]
    
    # Open data-file for writing
    f_out = open('./data/' + user_type + '_data.txt','w')
    
    # Collect tweets using Twitter API
    twitter = OAuth1Session(keys[0], keys[1], keys[2], keys[3])
    for target_user in user_list:
        params = {'screen_name':target_user,
                'exclude_replies':False,
                'include_rts':True,
                'count':100,
                'since_id':since_id}
        res = twitter.get(url, params = params)
        # If error(code != 200)
        if res.status_code != 200:
            print(target_user + ' got a error.')
            continue
        # If code == 200(nomal)
        # Display remaining number of API limit
        limit = res.headers['x-rate-limit-remaining']
        print ("API limit remaining: " + limit)
        if limit == 1:
            sleep(60*15)
        # Get timeline
        timeline = json.loads(res.text)
        # Display zero-tweet user
        if len(timeline) == 0:
            print(target_user + ' has 0 tweet.')
        # write to file
        for i in range(len(timeline)):
            text_i = timeline[i]['text']
            text_i = text_i.replace('\n', ' ')
            f_out.write(timeline[i]['created_at'] + ' @' + target_user + '@ ' + text_i + '\n')
    f_out.close()
    sleep(1)

# main
user_type = 'all'
# If today is a holiday then end with rc=255
holiday_func.is_holiday()
# Get tweets using twitter API and generate ./data/xxxx_data.txt
getweet(user_type, 1, 17)
# Get tokenized_text from ./data/xxxx_data.txt
tokenized_text = extract_func.extract_ticker(user_type)
print('==============================================')
# Extract tickers and save to ticker_list
ticker_list = extract_func.ext_ticker.findall(tokenized_text)
# Create a Counter object and display counting result
cnt = Counter(ticker_list).most_common()
print(cnt)
# Pickle objects(input data of Step02/03)
to_pickle(tokenized_text, 'tokenized_text.pkl')
to_pickle(cnt, 'cnt.pkl')
sleep(1)
print('==============================================')
print('            Step01 completed!')
print('==============================================')
