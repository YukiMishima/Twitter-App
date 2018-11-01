import json, config
from requests_oauthlib import OAuth1Session
import pandas as pd

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

params = {'count':5}
res = twitter.get(url, params = params)

columns = ['time', 'tweet']
df = pd.DataFrame(columns=columns)

if res.status_code == 200:
    timelines = json.loads(res.text)
    for tweet in timelines:
        text = tweet['text']
        created_at = tweet['created_at']
        append_list = [created_at, text]
        df_next = pd.DataFrame([append_list], columns = columns)
        df = df.append(df_next)
    #print(df)
    df.to_csv("C:/Users/amaga/Dropbox/twitter_app/new_tweets.csv", encoding = 'utf-8_sig')
else:
    print("Failed: %d" % res.status_code)