from constants import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, TWITTER_BEARER_TOKEN

import tweepy
import time
import datetime


client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    bearer_token=TWITTER_BEARER_TOKEN,
    wait_on_rate_limit=True
)

auth = tweepy.OAuth1UserHandler(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
    )

api = tweepy.API(auth)


RESPONDER_ID = 1650231286215196679

last_tweet_request = []
last_like_request = []


def sleeper(limit, request_list):
    current_time = datetime.datetime.now()
    request_rollover = None

    if request_list:
        request_rollover = request_list[0] + datetime.timedelta(minutes=15)
        if request_rollover <= current_time:
            request_list.pop(0)

    if len(request_list) >= limit and request_rollover and request_rollover >= current_time:
        oldest_request = request_list.pop(0)
        print("too many requests eepy now " + current_time.strftime("%d/%m/%Y %H:%M:%S"))
        sleep_length = (datetime.timedelta(minutes=15) - (current_time - oldest_request)).total_seconds() + 30
        print("sleeping for " + str(sleep_length/60) + " minutes")
        print("I'll wake up at " + (current_time + datetime.timedelta(seconds=sleep_length)).strftime(
            "%d/%m/%Y %H:%M:%S"))
        time.sleep(sleep_length)


def get_tweets(query, next_token=None, since_id=None, expansions=None):
    return client.search_recent_tweets(query=query, next_token=next_token, since_id=since_id, expansions=expansions)


def tweet(text, tweet_id, user_id, media_key, tweeted, liked):
    global last_tweet_request
    global last_like_request
    if user_id != RESPONDER_ID:
        print(tweeted)
        if not liked:
            sleeper(50, last_like_request)
            client.like(tweet_id=tweet_id)
            last_like_request.append(datetime.datetime.now())
        sleeper(200, last_tweet_request)
        if media_key:
            media_id = api.media_upload(filename=media_key)
            client.create_tweet(text=text, media_ids=[media_id.media_id_string], in_reply_to_tweet_id=tweet_id)
        else:
            client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
            last_tweet_request.append(datetime.datetime.now())
            print("\nLiked & radbro sent")
