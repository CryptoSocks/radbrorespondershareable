from tweeter import tweet, get_tweets, sleeper
import regex as re
import time
import datetime

query = '(radbro OR radbros OR Radbro OR Radbros) -is:retweet'
expansions = 'author_id'
last_requests = []


def loop_responses(response, since_id):
    global last_requests
    meta_params = response.meta
    if meta_params['result_count'] == 0:
        print("no new tweets sleep 1.5 min")
        time.sleep(90)
        return since_id
    else:
        print("\nThe response has " + str(len(response.data)) + " tweets\n")
        for response_line in response.data:
            if response_line:
                text = response_line['text'].lower()
                text = re.sub(r"(?:\@|https?\://)\S+", "", text)
                user_id = response_line['author_id']
                tweet_id = response_line['id']
                try:
                    if "radbro" in text:
                        tweet(text='radbro', tweet_id=tweet_id, user_id=user_id, tweeted=text)
                except Exception as e:
                    print(e)
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