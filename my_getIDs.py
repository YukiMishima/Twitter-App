import tweepy
import os
import pandas
import time
import config

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

def getFollowerIdsList(search_id): #引数にツイッターID、リスト形式でフォロワーのツイッターIDを返す 

    followers_ids = tweepy.Cursor(api.followers_ids, id = search_id, cursor = -1).items()
    followers_ids_list = []

    try:
        for followers_id in followers_ids:
            followers_ids_list.append(followers_id)

    except tweepy.error.TweepError as e:
        print (e.reason)

    return followers_ids_list

if __name__ == "__main__":

    id_list = getSearchIdsList()
    all_ids = []

    for search_id in id_list:
        followerIdsList = getFollowerIdsList(search_id)
        followersCount = len(followerIdsList)
        count = 0
        for followerId in followerIdsList:
            try:
                userid = api.get_user(followerId).screen_name
                print('now searching id is ... ' + search_id)
                print('userid', userid)
                count += 1
                all_ids.append(userid)
            except:
                print("Failed to retrieve user...retry")
                time.sleep(10)
            print("progress : {}%".format(round((count/followersCount)*100)))
            print("++++++++++++++++++++++++")
    print(all_ids)