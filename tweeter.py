from constants import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, TWITTER_BEARER_TOKEN
import tweepy
from twython import Twython

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

twython = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

RESPONDER_ID = 1650231286215196679

followers = []


def check_user_follows(user_id):
    global followers
    if not any(user_id is str(follow.id) for follow in followers):
        followers = client.get_users_followers(id=RESPONDER_ID)[0]
        return any(user_id == str(follow.id) for follow in followers)
    else:
        return True


def tweet_custom(text, id): 
    status = client.get_tweet(id=id, expansions='author_id')
    user_id = status['user']['id']
    screen_name = status['user']['screen_name']
    user_follows = check_user_follows(user_id)
    if user_id != RESPONDER_ID and user_follows:
        print(f'{screen_name}, {screen_name} follows {user_follows}')
        client.create_tweet(text=text, in_reply_to_tweet_id=id)
        client.like(tweet_id=id)


def tweet(text, id, user_id):
    user_follows = check_user_follows(user_id)
    if user_id != RESPONDER_ID and user_follows:
        print("they follow you, watch out!")
        """
        if text == '420':
            media = api.media_upload(f'memes/miladyblunt.jpeg')
            client.create_tweet(text='BLAZE IT', media_ids=[media.media_id], in_reply_to_tweet_id=id)
        else:
        """
        client.create_tweet(text=text, in_reply_to_tweet_id=id)
        client.like(tweet_id=id)
        print("tweet sent")
