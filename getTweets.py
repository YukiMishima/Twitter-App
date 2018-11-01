import json, config
from requests_oauthlib import OAuth1Session
import pandas as pd
from time import sleep

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

count = 100
params = {'count':count}

columns = ['time', 'tweet']
df = pd.DataFrame(columns=columns)

while True:
    res = twitter.get(url, params=params)
    
    if res.status_code == 200:
        timelines = json.loads(res.text)
        if timelines:
            for tweet in timelines:
                text = tweet['text']
                created_at = tweet['created_at']
                append_list = [created_at, text]
                df_next = pd.DataFrame([append_list], columns = columns)
                df = df.append(df_next)
            max_id = timelines[-1]['id']
            print(max_id)
            params['max_id'] = max_id -1
        else:
            print('collecting your all tweets was completed')
            break
    else:
        print('your reqest is limited by TwitterAPI, so it is suspended for 15min')
        for i in range(15):
            sleep(60)
            print(str(i+1)+'minutes have passed')
        print('your request is resumed')

df.to_csv("tweets.csv", encoding = 'utf-8_sig')