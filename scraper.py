import requests
import json


def get_post_json(post_id: str, count_of_best_comments: int) -> list:
    result = ['', []]
    r = requests.get(
        f'https://reddit.com/comments/{post_id}.json', headers={'user-agent': 'you should work'})

    print(r.status_code)
    if r.status_code != 200:
        exit(r.status_code)

    js = json.loads(r.text)

    title = js[0]['data']['children'][0]['data']['title']
    comments = js[1]['data']['children']
    result[0] = title

    comments_texts = []

    for comment in comments:
        comments_texts.append([comment['data'].get('ups', 0), comment['data'].get('body', '')])

    comments_texts.sort(reverse=True)

    for index in range(count_of_best_comments):
        result[1].append(comments_texts[index][1])

    return result
