import tweepy
import numpy as np
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
 
# Consumer keys and access tokens, used for OAuth
consumer_key = 'XXXXXXX'
consumer_secret = 'XXXXXX'
access_token = 'XXXXXXX'
access_token_secret = 'XXXXXXXX'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
#s = api.search(q="@peta", in_reply_to_status_id = "1098992959649808384", 
               #count = 100, max_id=str(last_id - 1))

#for tweets in s:
    #if tweets.lang == "en":
        #print ("Tweet text:", tweets.text)
max_tweets = 5000
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q="@peta", in_reply_to_status_id = "1098992959649808384", 
               count = count, lang = "en", max_id=str(last_id - 1),
               in_reply_to_user_id_str = "9890492", tweet_mode = "extended")
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

sia = SentimentIntensityAnalyzer()
scores = np.array([])
for tweet in searched_tweets:
    isRT = hasattr(tweet, 'retweeted_status')
    if isRT == False:
        score = sia.polarity_scores(tweet.full_text)["compound"]
        scores = np.append(scores, score)
plt.hist(scores, bins = 3)
