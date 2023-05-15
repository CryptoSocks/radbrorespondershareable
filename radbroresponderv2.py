from constants import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, TWITTER_BEARER_TOKEN
import requests
import json
from tweeter import tweet
import regex as re
import time
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = TWITTER_BEARER_TOKEN


search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(radbro OR radbros OR Radbro OR Radbros -is:retweet)', 'expansions': 'author_id', 'max_results': '100'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def loop_responses(response, previous_id):
    meta_params = response.json()['meta']
    if meta_params['result_count'] == 0:
        print("no new tweets sleep 3 min")
        time.sleep(180)
        return previous_id
    else:
        for response_line in response.json()['data']:
            if response_line:
                text = response_line['text'].lower()
                text = re.sub(r"(?:\@|https?\://)\S+", "", text)
                text = text.replace(" ", "")
                user_id = response_line['author_id']
                id = response_line['id']
                print("author id: " + user_id)
                print(text)
                try:
                    if "radbro" in text:
                        tweet(text='radbro', id=id, user_id=user_id)
                except Exception as e:
                    print(e)
        return meta_params['newest_id']

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    for response_line in response.json()['data']:
        if response_line:
            text = response_line['text'].lower()
            text = re.sub(r"(?:\@|https?\://)\S+", "", text)
            text = text.replace(" ", "")
            user_id = response_line['author_id']
            id = response_line['id']
            print("author id: " + user_id)
            print(text)
            try:
                if "radbro" in text:
                    tweet(text='radbro', id=id, user_id=user_id)
            except Exception as e:
                print(e)

def tl_stream(url):
    query_params = {'query': '(radbro OR radbros OR Radbro OR Radbros -is:retweet)', 'expansions': 'author_id'}
    previous_id = False
    r = 0
    while True:
        if r > 15:
            r = 0
            print("too much searchy eepy now " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print("wake me up at " + (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime("%d/%m/%Y %H:%M:%S"))
            time.sleep(900)
        response = requests.get(url, auth=bearer_oauth, params=query_params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        query_params['since_id'] = previous_id = loop_responses(response, previous_id)
        r += 1

def main():
    tl_stream(search_url)
    """
    connect_to_endpoint(search_url, query_params)
    """

if __name__ == "__main__":
    main()