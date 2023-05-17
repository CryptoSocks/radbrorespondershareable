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

RESPONDER_ID = 1650231286215196679

followers = []
last_follow_request = [datetime.datetime.now() - datetime.timedelta(minutes=6)]
last_tweet_request = []
last_like_request = []

"""
current time 1:50pm
time of earliest request 1:45pm
if 1:45pm+ 15 min (2pm) is greater than or equal to 1:50pm
"""


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

def check_user_follows(user_id):
    global followers
    global last_follow_request

    if not any(user_id == follow.id for follow in followers):
        if datetime.datetime.now() - last_follow_request[-1] <= datetime.timedelta(minutes=5):
            return False
        sleeper(15, last_follow_request)
        followers = client.get_users_followers(id=RESPONDER_ID, max_results=1000)[0]
        last_follow_request.append(datetime.datetime.now())
        return any(user_id == follow.id for follow in followers)
    else:
        return True


def tweet(text, tweet_id, user_id, tweeted):
    global last_tweet_request
    global last_like_request
    global followers
    user_follows = check_user_follows(user_id)
    if user_id != RESPONDER_ID and user_follows:
        username = [user.name for user in followers if user.id == user_id]
        """
        if text == '420':
            media = api.media_upload(f'memes/miladyblunt.jpeg')
            client.create_tweet(text='BLAZE IT', media_ids=[media.media_id], in_reply_to_tweet_id=id)
        else:
        """
        sleeper(50, last_like_request)
        sleeper(200, last_tweet_request)
        print("\n" + username[0] + " said:\n")
        print(tweeted)
        client.like(tweet_id=tweet_id)
        last_like_request.append(datetime.datetime.now())
        client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        last_tweet_request.append(datetime.datetime.now())
        print("\nLiked & radbro sent")
