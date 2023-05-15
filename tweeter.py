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

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


RESPONDER_ID = 1650231286215196679

followers = []
rf = 0
rt = 0
rl = 0


def check_user_follows(user_id):
    global followers
    global rf

    print("follow " + str(rf))
    if rf < 15:
        rf += 1
    else:
        rf = 0
        print("too much follow eepy now " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("wake me up at " + (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime("%d/%m/%Y %H:%M:%S"))
        time.sleep(900)
    if not any(user_id is str(follow.id) for follow in followers):
        followers = client.get_users_followers(id=RESPONDER_ID)[0]
        return any(user_id == str(follow.id) for follow in followers)
    else:
        return True


def tweet(text, id, user_id):
    global rt
    global rl
    user_follows = check_user_follows(user_id)
    if user_id != RESPONDER_ID and user_follows:
        print("they follow you, watch out!")
        """
        if text == '420':
            media = api.media_upload(f'memes/miladyblunt.jpeg')
            client.create_tweet(text='BLAZE IT', media_ids=[media.media_id], in_reply_to_tweet_id=id)
        else:
        """

        print("tweet " + str(rt))
        print("like " + str(rl))
        if rt < 200:
            rt += 1
        else:
            rt = 0
            print("too much tweety eepy now " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print("wake me up at " + (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime(
                "%d/%m/%Y %H:%M:%S"))
            time.sleep(900)
        if rl < 50:
            rl += 1
        else:
            rl = 0
            print("too much likey eepy now " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print("wake me up at " + (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime(
                "%d/%m/%Y %H:%M:%S"))
            time.sleep(900)
        client.create_tweet(text=text, in_reply_to_tweet_id=id)
        client.like(tweet_id=id)
        print("tweet sent")
