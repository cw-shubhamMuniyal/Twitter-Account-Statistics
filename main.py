import pandas as pd  # To handle data
import numpy as np  # For number computing
import math
from flask import Flask, render_template, jsonify, request
from datetime import datetime
import tweepy

# For plotting and visualization:
# from IPython.display import display
import matplotlib.pyplot as plt

# import seaborn as sns
from textblob import TextBlob
import re
import twitter
import json

# %matplotlib inline

# We import our access keys:
from keys import *  # This will allow us to use the keys as variables

listlikes_ = [0, 0, 0]
listRetweets = [0, 0, 0]
# API's setup:


def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Return API with authentication:
    api = tweepy.tweepy.API(auth)
    return api


WORLD_WOE_ID = 1
auth = twitter.oauth.OAuth(
    access_token, access_token_secret, consumer_key, consumer_secret
)


twitter_api = twitter.Twitter(auth=auth)
trends1 = twitter_api.trends.place(_id=WORLD_WOE_ID)


# Prefix ID with the underscore for query string parameterization.
# Without the underscore, the twitter package appends the ID value
# to the URL itself as a special case keyword argument.

"""trends1 = twitter_setup().trends_place(WORLD_WOE_ID) # from the end of your code
# trends1 is a list with only one element in it, which is a
#

# trends1 is a list with only one element in it, which is a
# dict which we'll put in data."""
data = trends1[0]
# grab the trends
trends = data["trends"]
# grab the name from each trend
names = [trend["name"] for trend in trends]
# put all the names together with a ' ' sepa
# rating them
"""for name in names:
    print(name)"""


def clean_tweet(tweet):
    """
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    """
    return " ".join(
        re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()
    )


def analize_sentiment(tweet):
    """
    Utility function to classify the polarity of a tweet
    using textblob.
    """

    analysis = TextBlob(clean_tweet(tweet))
    """if analysis.detect_language() != 'en':
        analysis.translate(to='en')"""

    return analysis


# def returnSomeInformation(tweet):
# We create an extractor object:
# WORLD_WOE_ID = 1
# world_trends = twitter_setup().trends.place(_id=WORLD_WOE_ID)
# print(world_trends)


app = Flask(__name__)


@app.route("/charts", methods=["GET", "POST"])
def charts():
    extractor = twitter_setup()
    listlikes_ = [0, 0, 0]
    listRetweets = [0, 0, 0]

    # We create a tweet list as follows:
    name = request.form["accountHolder"]
    if name[0] == "#":
        name = name[1:]
    name = name.replace(" ", "")

    # name = "realDonaldTrump"
    number = 0
    positive = 0
    negative = 0
    neutral = 0
    # number = int(input("Enter Number of tweets"))

    # tweets = extractor.user_timeline(screen_name=name, count=number)
    # print("Number of tweets extracted: {}.\n".format(len(tweets)))

    # We print the most recent 5 tweets:
    try:
        print(" recent tweets:\n")
        tweets = extractor.user_timeline(screen_name=name, count=200)
        # tweets = tweepy.tweepy.Cursor(extractor.user_timeline, id=name).items()

        file = open("tweet.json", "wb")

        for tweet in tweets:

            with open("tweet.json", "a", encoding="utf8") as file:
                json.dump(tweet._json, file)
                file.write("\n \n \n")

            print(clean_tweet(tweet.text))
            print(tweet.favorite_count)
            print("\n")

            if tweet.favorite_count < 500:
                listlikes_[0] = listlikes_[0] + 1
            elif tweet.favorite_count > 500 and tweet.favorite_count < 1000:
                listlikes_[1] = listlikes_[1] + 1
            else:
                listlikes_[2] = listlikes_[2] + 1

            if tweet.retweet_count < 500:
                listRetweets[0] = listRetweets[0] + 1
            elif tweet.retweet_count > 500 and tweet.retweet_count < 1000:
                listRetweets[1] = listRetweets[1] + 1
            elif tweet.retweet_count > 1000:
                listRetweets[2] = listRetweets[2] + 1
            """df2=pd.DataFrame(data=[tweet.favorite_count,tweet.retweet_count,tweet.created_at],columns=['likes','retweets','source'])
            #df2.append(df1)"""

            sentimental = analize_sentiment(tweet.text)
            pol = analize_sentiment(tweet.text).sentiment.polarity
            sub = analize_sentiment(tweet.text).sentiment.subjectivity

            if pol > 0:
                print("tweet is positive")
                sentiment = "positive"
                positive += 1

            elif pol < 0:
                print("tweet is negative")
                sentiment = "negative"
                negative += 1

            else:
                print("tweet is neutral")
                sentiment = "neutral"
                neutral += 1

            number = number + 1
            print("\n")

        print(number, "of tweets are collected")
        print("sentimental analysis:\n")
        print("percentage of sentiment=\n")

        print("positive tweets= %s" % (positive * 100 / number), "%")
        sentimentp = math.floor(positive * 100 / number)

        print("neutral tweets= %s" % (neutral * 100 / number), "%")
        sentimentn = math.floor(neutral * 100 / number)

        print("negative tweets= %s" % (negative * 100 / number), "%")
        sentimentne = math.floor(negative * 100 / number)
        print(listlikes_)
        print(listRetweets)

        sentimentList = [sentimentp, sentimentn, sentimentne]
        return render_template(
            "charts.html",
            listlikes_=listlikes_,
            sentimentList=sentimentList,
            listRetweets=listRetweets,
        )

    except tweepy.tweepy.TweepError:
        pass


@app.route("/data")
def data():
    return jsonify({"likes_": listlikes_})


@app.route("/")
def index():
    global names
    return render_template("twitterTakeAccount.html", names_=names)


if __name__ == "__main__":
    app.run(debug=True)

    # print(df2)
    # We create a pandas dataframe as follows:
