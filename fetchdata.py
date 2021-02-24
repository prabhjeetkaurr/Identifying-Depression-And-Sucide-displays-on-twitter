import re
import tweepy as tw
import pandas as pd
from textblob import TextBlob, Word


# Twitter-API-Tokens
consumer_key= 'tKE2eP4NnD7JM2JqWYNnYRtVj'
consumer_secret= 'TTGodvnFnzARrMWSBY5vrbfbtVkau3ZPLCFEjKAqbC1ebRc6Jm'
access_token= '3904542806-TJo4WPYkjTVH3IQdpDk8obA8NpXEnFjijzXzEiM'
access_token_secret= 'vQDmnZkDPM7DlwTCMFwzGXghIJL6tcMJz76UFQMLpHwmU'


# Code
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def auth():
    try:
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except Exception as e:
        print(e)
        return None

auth = auth()
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "#depression OR depression OR #suicide OR suicide OR #depressing OR depressing OR #depressed OR depressed OR #suicidal OR suicidal " + "-filter:retweets"
date_since = "2015-01-01"


def FetchTrainTweets():
    print('--In user Details Function--')
    # Collect tweets
    tweets = tw.Cursor(api.search,
        q=search_words,
        lang="en",
        since=date_since).items(5000)

    userTweets = pd.DataFrame([tweet.user.name,tweet.user.screen_name,tweet.user.description,tweet.user.friends_count,tweet.user.followers_count,tweet.user.location,remove_url(tweet.text)] for tweet in tweets)
    userTweets.columns=['name','id','description','friends','followers','location','tweet']
    userTweets.to_csv("train_data.csv" ,header=True, index=True, encoding='utf-8')

#Fetch Train Data
FetchTrainTweets()

