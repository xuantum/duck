# tweet_msg() tweets a message. You can post a message with a image using the optional argument "file".
import json
from requests_oauthlib import OAuth1Session
from time import sleep

def tweet_msg(keys, message, file=''):
    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"
    def post(params):
        req = twitter.post(url_text, params = params)
        if req.status_code == 200:
            print('Tweeted!')
            sleep(5)
        else:
            print('ERROR in tweet: %d' % req.status_code)
    # Start connecting
    #twitter = OAuth1Session(consumer_key, consumer_key_secret, access_token, access_token_secret)
    twitter = OAuth1Session(keys[0], keys[1], keys[2], keys[3])

    # Tweet a message without a image
    if file == '':
        params = {'status': message}
        post(params)
        return
    
    # Tweet a message with a image
    # Get a image
    with open(file, 'rb') as img:
        data = img.read()
    files = {"media" : data}
    # Upload a image
    req = twitter.post(url_media, files = files)
    # If error occur(code!=200)
    if req.status_code != 200:
        print('ERROR in uploading: %d' % req.status_code)
        return
    # If no error(code==200)
    print('Image uploaded.')
    # Get "media_id"
    media_id = json.loads(req.text)['media_id']
    sleep(3)
    # Tweet a messsage with "media_ids"
    params = {'status': message, "media_ids": [media_id]}
    post(params)
