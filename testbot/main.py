# coding: utf-8

import os
import requests
import random
import json

ADDR = os.environ.get('ADDRESS', 'http://localhost:8001')

def main():
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

    users_num = config['number_of_users']
    user_max_posts = config['max_posts_per_user']
    user_max_likes = config['max_likes_per_user']

    for n in range(0, users_num):
        requests.put(ADDR + '/api/account/',
                     data=json.dumps({'username': 'test' + str(n),
                                 'password': 'P@$$'}),
                     headers={'Content-Type': 'application/json'})

        auth = requests.post(ADDR + '/api/token/',
                             data=json.dumps({'username': 'test' + str(n),
                                   'password': 'P@$$'}),
                             headers={'Content-Type': 'application/json'})
        token = auth.json()['access']

        posts_num = random.randint(0, user_max_posts)
        for i in range(0, posts_num):
            requests.put(ADDR + '/api/post/',
                         data=json.dumps({'name': str(n) + '_test post_' + str(i),
                               'description': 'Some description for post ' + str(n) + str(i)}),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + token})

    for n in range(0, users_num):
        auth = requests.post(ADDR + '/api/token/',
                             data=json.dumps({'username': 'test' + str(n),
                                   'password': 'P@$$'}),
                             headers={'Content-Type': 'application/json'})
        token = auth.json()['access']
        posts = requests.get(ADDR + '/api/post/',
                             headers={'Content-Type': 'application/json',
                                      'Authorization': 'Bearer ' + token})
        posts = posts.json()['results']
        user_likes = random.randint(0, user_max_likes)
        liked_posts = []
        for p in range(0, user_likes):
            p = random.randint(0, len(posts) - 1)
            if liked_posts:
                while p in liked_posts:
                    p = random.randint(0, len(posts) - 1)
            requests.put(ADDR + '/api/like/',
                          data=json.dumps({'post': posts[p]['id']}),
                          headers={'Content-Type': 'application/json',
                                   'Authorization': 'Bearer ' + token})
            liked_posts.append(p)

    return

if __name__ == '__main__':
    main()
