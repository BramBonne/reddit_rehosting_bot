__author__ = 'bram'

import praw
from time import sleep

REHOSTING_DOMAINS = ['imgur.com', 'imageshack.com']

api = praw.Reddit('A bot for delivering source by /u/gooz and /u/piratenaapje')
api.login('sneaky_emil', 'x4mSCwy1UNZV')
subreddits = api.get_subreddit('images')
processed = set()
commented_on = set()
round = 1
while True:
    print "\rRound %d: commented %d times" % (round, len(commented_on)),
    hot_submissions = set(subreddits.get_hot(limit=50))
    for submission in (hot_submissions - processed):
        if any(rehosting_domain in submission.url for rehosting_domain in REHOSTING_DOMAINS):
            try:
                #submission.add_comment("Test comment, please ignore.")
                # TODO: check for source and reply as per previous line
                print "Replied to submission %s" % submission.title
                commented_on.add(submission.id)
            except praw.errors.RateLimitExceeded as e:
                print "\rComment rate limit temporarily exceeded (%s), deferring until next round." % repr(e)
                sleep(60) # Prevent reddit from incurring a penalty
                continue # Handle next item in the list
        processed.add(submission.id)
    sleep(2)
    round += 1