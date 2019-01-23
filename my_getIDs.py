import tweepy
import os
import pandas
import time
import config

# search_id = "chilffy" #ツイッターのID
df = pandas.read_csv('default.csv', index_col=0)
count = 0
skip = 0

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth ,wait_on_rate_limit = True)

def getSearchIdsList(): #標準入力から入力されたサーチしてほしいIDをリストにして返す
    search_ids = []
    inputed_id = ''
    while True:
        print('enter ID')
        inputed_id = input()
        if inputed_id == 'end':
            break
        else:
            search_ids.append(inputed_id)
    return search_ids

def getFollowerIdsList(search_id): #引数にツイッターID、リスト形式でフォロワーのツイッターIDを返します  

    followers_ids = tweepy.Cursor(api.followers_ids, id = search_id, cursor = -1).items()
    followers_ids_list = []

    try:
        for followers_id in followers_ids:
            followers_ids_list.append(followers_id)

    except tweepy.error.TweepError as e:
        print (e.reason)

    return followers_ids_list

def getFollowers(userID): #ユーザーIDを指定して、フォロワー数を返します
    user = api.get_user(userID)
    followersCount = user.followers_count
    return followersCount

def getFollowings(userID): #ユーザーIDを指定して、フォロー数を返します
    user = api.get_user(userID)
    followingCount = user.friends_count
    return followingCount

if __name__ == "__main__":

    id_list = getSearchIdsList()

    for search_id in id_list:
        followerIdsList = getFollowerIdsList(search_id)
        followersCount = len(followerIdsList)
        count = 0
        skip = 0
        for followerId in followerIdsList:
            try:
                userid = api.get_user(followerId).screen_name
                followers = getFollowers(followerId)
                followings = getFollowings(followerId)
                se = pandas.Series([userid, followers, followings],['userid','followers','followings'])
                print('now searching id is ... '+search_id)
                print(se)
                count += 1
                print("{}%".format((count + skip) / followersCount)*100)
                print('++++++++++++++++++++')
                df = df.append(se, ignore_index=True)
            except:
                print("Failed to retrieve user...retry")
                skip += 1
                print("{}%".format(round((count + skip) / followersCount)*100))
                time.sleep(10)
        df.to_csv("{}.csv".format(search_id)) # pandasでcsvに保存する