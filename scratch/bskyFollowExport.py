#!/usr/bin/env python3

import os

MY_HANDLE = 'chaosbengel.de'
PASS = os.environ.get('BSKY_APP_PASS')

from atproto import Client, models, IdResolver
from sys import argv

client = Client()
resolver = IdResolver()
target = argv[1]
outfile = argv[2]

client.login(MY_HANDLE, PASS)



cursor = None
with open(outfile, 'w', encoding='utf-8') as f:
    while True:
        response = client.app.bsky.graph.get_followers(
            models.AppBskyGraphGetFollowers.Params(
                actor=target,
                limit=100,
                cursor=cursor
            )
        )
        cursor = response.cursor
        for follower in response.followers:
            f.write(follower.did + '\n')
        if cursor is None:
            break

