import pandas as pd
import datetime

csv_init = pd.read_csv('data/tweets.csv',encoding='utf-8')
csv_init.to_csv('data/tweet_utf16.csv',encoding='utf-16')

df = pd.read_csv('data/tweet_utf16.csv', encoding='utf-16')

jst_list = []
for index, row in df['timestamp'].iteritems():
    utc = datetime.datetime.strptime(row, '%Y-%m-%d %H:%M:%S +0000')
    jst = utc + datetime.timedelta(hours=9)
    jst_list.append(jst)

jst_series = pd.Series(jst_list)
df_TimeText = pd.concat([jst_series, df['text']], axis=1)

df_TimeText.to_csv('data/time_txt.csv', encoding='utf-16')