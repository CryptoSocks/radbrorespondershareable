from constants import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, TWITTER_BEARER_TOKEN
import requests
import json
from tweeter import tweet
import regex as re  
from twython import Twython

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = TWITTER_BEARER_TOKEN
twython = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(radbro OR radbros OR Radbro OR Radbros -is:retweet)', 'expansions': 'author_id'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

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
            if "radbro" in text or 'rad' in text or 'radbros' in text:
                try:
                    if "radbro" in text:
                        tweet(text='radbro', id=id, user_id=user_id)
                except Exception as e:
                    print(e)



def main():
    connect_to_endpoint(search_url, query_params)


if __name__ == "__main__":
    main()