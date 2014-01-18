__author__ = 'bram'

import praw
from time import sleep

api = praw.Reddit('A bot for testing the reddit API by /u/gooz')
api.login('sneaky_emil', 'x4mSCwy1UNZV')
subreddits = api.get_subreddit('wtf+japan')
commented_on = set()
round = 1
while True:
    print "\rRound %d: commented %d times" % (round, len(commented_on)),
    comments = subreddits.get_comments()
    for comment in comments:
        if 'japan' in comment.body.lower() and comment.id not in commented_on:
            comment.reply("Ah, Japan.")
            print "Replied to comment %s" % comment.body
            commented_on.add(comment.id)
    sleep(2)
    round += 1