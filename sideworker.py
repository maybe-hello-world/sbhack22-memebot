import os
import json
import random

import requests


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    search_phrase = request_json['search_phrase']
    full_phrase = request_json['full_phrase']

    catch_phrazes = ["What about",
                     "Remember that",
                     "What Chancellor Yang says about",
                     "Have you seen",
                     ]
    num_results = 5

    url = f"https://customsearch.googleapis.com/customsearch/v1/?" \
          f"key={os.environ['APIKEY']}&" \
          f"cx={os.environ['cxid']}&" \
          f"num={num_results}&" \
          f"q={search_phrase + ' meme'}&" \
          f"searchType=image"
    r = requests.get(url)
    if r.status_code != 200:
        return -1
    response = json.loads(r.text)

    url = [i["link"] for i in response["items"]][random.randint(0, num_results - 1)]

    baseURL = f"https://discordapp.com/api/channels/{os.environ['channel_id']}/messages"
    headers = {"Authorization": f"Bot {os.environ['TOKEN']}",
               "User-Agent": "myBotThing (http://some.url, v0.1)",
               "Content-Type": "application/json", }
    payload = {
        "content": f"{random.choice(catch_phrazes)} {search_phrase} meme?",
        "embeds": [
            {
                "image": {
                    "url": url
                }
            }
        ]
    }

    POSTedJSON = json.dumps(payload)

    r = requests.post(baseURL, headers=headers, data=POSTedJSON)

    return url

