from dotenv import load_dotenv
import os
import tweepy
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from random import shuffle
import socket
import time

load_dotenv()

consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_secret = os.environ.get('access_secret')

# authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

sia = SentimentIntensityAnalyzer()
# def is_positive(tweet):
#     """True if tweet has positive compound sentiment, False otherwise."""
#     print(sia.polarity_scores(tweet))
#     if(sia.polarity_scores(tweet)['compound'] > 0):
#         return 1
#     elif(sia.polarity_scores(tweet)['compound'] < 0):
#         return -1
#     else:
#         return 0

columns = ['Time', 'User', 'Tweet']
data = []
for tweet in public_tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

df = pd.DataFrame(data, columns=columns)
# df['Polarity'] = df['Tweet'].apply(is_positive)
df.to_csv('tweets.csv')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostbyname("localhost"), 9999))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} established !!!")
    with open("tweets.csv", "r", encoding="utf-8") as f:
        for line in f:
            clientsocket.send(bytes(line, "utf-8"))
            time.sleep(3)


