import twitter
import tweepy
from keys import *
import json
# The Yahoo! Where On Earth ID for the entire world is 1.
# See https://dev.twitter.com/docs/api/1.1/get/trends/place and
# http://developer.yahoo.com/geo/geoplanet/


auth = tweepy.tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Return API with authentication:
api = tweepy.tweepy.API(auth)


WORLD_WOE_ID = 1

# Prefix ID with the underscore for query string parameterization.
# Without the underscore, the twitter package appends the ID value
# to the URL itself as a special case keyword argument.

trends1 = api.trends_place(WORLD_WOE_ID) # from the end of your code
# trends1 is a list with only one element in it, which is a
#

# trends1 is a list with only one element in it, which is a
# dict which we'll put in data.
data = trends1[0]
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
# put all the names together with a ' ' separating them
print(names[0])
trendsName = '\n'.join(names)
print(trendsName)