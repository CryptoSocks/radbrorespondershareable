import os
from tweeter import tweet, get_tweets, sleeper_v2
import regex as re
import time
import datetime

query = '(radbro OR radbros OR radbroresponder OR radcat OR 拉德兄弟 OR 拉德猫) -is:retweet'
expansions = 'author_id'
last_requests = []


def send_tweet(text, tweet_id, user_id, tweeted, liked=False, media_key=None):
    try:
        tweet(text=text, tweet_id=tweet_id, user_id=user_id, tweeted=tweeted, liked=liked, media_key=media_key)
    except Exception as e:
        print("Error posting reply:", e)


def process_tweet_v2(tweet_response):
    text = tweet_response['text'].lower()
    text = re.sub(r"(?:\@|https?\://)\S+", "", text)
    user_id = tweet_response['author_id']
    tweet_id = tweet_response['id']
    reply = ''
    media = None
    multi_reply = False
    shilling = False
    love = ["ily", "ilu", "i love you", "i love u"]
    over = ["its over", "it's over", "it's so over", "its so over"]
    esoterics = "radbro webring is faustian apollonian olympian the extension of infinite space the struggle against elementary chthonic forces the construction of grand murals in his glory the war to subdue lower projects its a quintessentially aryan experience"
    if "拉德兄弟" in text:
        media = "./pics/radbroChinese.png"
    elif "拉德猫" in text:
        media = "./pics/radcatChinese.png"
    elif "radcat" in text:
        if "420" in text:
            media = "./pics/420.jfif"
        elif "1080" in text:
            media = "./pics/1080.jfif"
        elif "based" in text:
            media = "./pics/based.jpg_medium"
        elif "free video" in text:
            media = "./pics/radcatvideo.jfif"
        elif "check the chain" in text:
            media = "./pics/checkthechaincat.jfif"
        elif "lore" in text:
            media = "./pics/radcatlore.jpg_medium"
        elif "git em" in text:
            media = "./pics/catcum.jpg_large"
        else:
            media = "./pics/radcat.jfif"
    elif "radbro" in text:
        if "$rad" in text:
            send_tweet(
                text='Buy $RAD on Uniswap \n CA: 0xdDc6625FEcA10438857DD8660C021Cd1088806FB \n Link to Uniswap: https://app.uniswap.org/#/swap?outputCurrency=0xddc6625feca10438857dd8660c021cd1088806fb&chain=ethereum \n Link to Dexscreener: https://dexscreener.com/ethereum/0x704160cbd110bcc2b4bf5d71830e590bc5685d3a',
                tweet_id=tweet_id, user_id=user_id, tweeted=text)
            shilling = True
            multi_reply = True
        if "$bro" in text:
            send_tweet(
                text='Buy $BRO on Uniswap \n CA: 0x6e08B5D1169765f94d5ACe5524F56E8ac75B77c6 \n Link to Uniswap: https://app.uniswap.com/#/swap?inputCurrency=0xddc6625feca10438857dd8660c021cd1088806fb&outputCurrency=0x6e08B5D1169765f94d5ACe5524F56E8ac75B77c6&chain=ethereum \n Link to Dexscreener: https://dexscreener.com/ethereum/0x0110660ec3fede0425183efd88cf5c4341ffc304',
                tweet_id=tweet_id, user_id=user_id, tweeted=text, liked=multi_reply)
            shilling = True
        if not shilling:
            if any(love_expression in text for love_expression in love):
                reply = 'i love you, radbro'
            elif "put that on my" in text:
                reply = 'i put that on my radbro 😤'
                media = "./pics/radbro.png"
            elif "webring" in text:
                reply = esoterics
            elif "lawyer" in text:
                media = "./pics/lawyer.jfif"
            elif "deal" in text:
                media = "./pics/wagie.png_medium"
            elif "always has been" in text:
                media = "./pics/RWO.jfif"
            elif "🤯" and "🦍" in text:
                media = "./pics/mindblownape.jfif"
            elif "🤯" in text:
                media = "./pics/mindblown.jfif"
            elif "pump it" in text:
                media = "./pics/pumpit.png"
            elif "ratio" in text:
                media = "./pics/Ratio.png"
            elif "git em" in text:
                media = "./pics/cum.jpg_medium"
            elif "check the chain" in text:
                media = "./pics/checkthechain.png"
            elif "ssv1" in text:
                media = "./pics/union.jpg_large"
            elif any(over_expression in text for over_expression in over):
                media = "./pics/itsover.jpg_medium"
            else:
                reply = 'radbro'
    if not shilling:
        if reply != '' or media is not None:
            send_tweet(text=reply, tweet_id=tweet_id, user_id=user_id, tweeted=text, media_key=media)


def loop_responses(response, since_id):
    global last_requests
    meta_params = response.meta
    result_count = meta_params['result_count']

    if result_count == 0:
        print("no new tweets sleep 30 sec")
        time.sleep(30)
        return since_id

    print("\nThe response has " + str(result_count) + " tweets\n")
    for response_line in response.data:
        if response_line:
            process_tweet_v2(response_line)
    return meta_params['newest_id']


def loop_responses_v2(response, since_id):
    global last_requests
    meta_params = response.meta
    result_count = meta_params['result_count']

    if result_count == 0:
        print("no new tweets sleep 30 sec")
        time.sleep(30)
        return since_id

    print("\nThe response has " + str(result_count) + " tweets\n")
    for response_line in response.data:
        if response_line:
            process_tweet_v2(response_line)

    # Check if there are more pages of tweets
    if since_id is not None:
        while 'next_token' in meta_params:
            next_token = meta_params['next_token']
            print("Requests in the last 15 min: " + str(len(last_requests)))
            sleeper_v2(60, last_requests)
            response = get_tweets(query=query, expansions=expansions, since_id=since_id, next_token=next_token)
            last_requests.append(datetime.datetime.now())
            meta_params = response.meta
            result_count = meta_params['result_count']
            print("\nThe response has " + str(result_count) + " tweets\n")
            for response_line in response.data:
                if response_line:
                    process_tweet_v2(response_line)

    return meta_params['newest_id']


def tl_stream():
    global last_requests
    since_id = None
    while True:
        print("Requests in the last 15 min: " + str(len(last_requests)))
        sleeper_v2(60, last_requests)
        response = get_tweets(query=query, expansions=expansions, since_id=since_id)
        last_requests.append(datetime.datetime.now())
        since_id = loop_responses(response, since_id)


def tl_stream_v2():
    global last_requests
    since_id_file = "since_id.txt"

    # Load the since_id from file if it exists
    if os.path.exists(since_id_file):
        with open(since_id_file, "r") as f:
            since_id = f.read().strip()
    else:
        since_id = None

    while True:
        try:
            response = get_tweets(query=query, expansions=expansions, since_id=since_id)
            since_id = loop_responses_v2(response, since_id)
        except Exception as e:
            print(e)

        # Save the since_id to file
        with open(since_id_file, "w") as f:
            f.write(str(since_id))

        time.sleep(30)


def main():
    tl_stream()


if __name__ == "__main__":
    main()
