from tweeter import tweet, get_tweets, sleeper
import regex as re
import time
import datetime

query = '(radbro OR radbros OR Radbro OR Radbros OR radbroresponder) -is:retweet'
expansions = 'author_id'
last_requests = []


def send_tweet(text, tweet_id, user_id, tweeted, liked):
    try:
        tweet(text=text, tweet_id=tweet_id, user_id=user_id, tweeted=tweeted, liked=liked)
    except Exception as e:
        print("Error posting reply:", e)


def process_tweet(tweet_response):
    text = tweet_response['text'].lower()
    text = re.sub(r"(?:\@|https?\://)\S+", "", text)
    user_id = tweet_response['author_id']
    tweet_id = tweet_response['id']
    multi_reply = False
    if "radbro" in text:
        if "ily" or "ilu" or "i love you" or "i love u" in text:
            send_tweet(text='i love you, radbro', tweet_id=tweet_id, user_id=user_id, tweeted=text, liked=multi_reply)
        else:
            send_tweet(text='radbro', tweet_id=tweet_id, user_id=user_id, tweeted=text, liked=multi_reply)
        multi_reply = True
    if "$rad" in text:
        send_tweet(text='Buy $RAD on sushiswap \n CA: 0xdDc6625FEcA10438857DD8660C021Cd1088806FB \n Link to Sushiswap: https://app.sushi.com/swap?inputCurrency=ETH&outputCurrency=0xdDc6625FEcA10438857DD8660C021Cd1088806FB \n Link to Dexscreener: https://dexscreener.com/ethereum/0x39940ee99171cdbbfdbd540b987e778dba8734dd', tweet_id=tweet_id, user_id=user_id, tweeted=text, liked=multi_reply)
        multi_reply = True
    if "$bro" in text:
        send_tweet(text='Buy $BRO on sushiswap \n CA: 0x6e08B5D1169765f94d5ACe5524F56E8ac75B77c6 \n Link to Sushiswap: https://app.sushi.com/swap?inputCurrency=0xdDc6625FEcA10438857DD8660C021Cd1088806FB&outputCurrency=0x6e08B5D1169765f94d5ACe5524F56E8ac75B77c6 \n Link to Dexscreener: https://dexscreener.com/ethereum/0xa99245ebaf606644b4674994717b3efa098272fe', tweet_id=tweet_id, user_id=user_id, tweeted=text, liked=multi_reply)

def loop_responses(response, since_id):
    global last_requests
    meta_params = response.meta
    result_count = meta_params['result_count']

    if result_count == 0:
        print("no new tweets sleep 1.5 min")
        time.sleep(90)
        return since_id

    print("\nThe response has " + str(result_count) + " tweets\n")
    for response_line in response.data:
        if response_line:
            process_tweet(response_line)
    return meta_params['newest_id']


def tl_stream():
    global last_requests
    since_id = None
    while True:
        sleeper(180, last_requests)
        response = get_tweets(query=query, expansions=expansions, since_id=since_id)
        last_requests.append(datetime.datetime.now())
        since_id = loop_responses(response, since_id)


def main():
    tl_stream()
    """
    connect_to_endpoint(search_url, query_params)
    """

if __name__ == "__main__":
    main()