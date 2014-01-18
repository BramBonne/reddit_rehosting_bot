__author__ = 'bram'

import praw
import pyimgur
from requests.exceptions import HTTPError
from time import sleep
from cStringIO import StringIO
import sys

IMGUR_API_KEY = ""
REDDIT_USERNAME = ""
REDDIT_PASSWORD = ""

def imgur_rehost_image(url, title):
    # Suppress command line output from module
    rehost_url = imgur_api.upload_image(url=url, title=title).link
    return rehost_url

api = praw.Reddit('A bot rehosting images on imgur.com by /u/gooz and /u/piratenaapje')
api.login(REDDIT_USERNAME, REDDIT_PASSWORD)
imgur_api = pyimgur.Imgur(IMGUR_API_KEY)
subreddits = api.get_subreddit('pics+images+gifs+reactiongifs+AdviceAnimals')
processed = set()
commented_on = set()
round = 1
while True:
    print "\rRound %d: commented %d times" % (round, len(commented_on)),
    hot_submissions = set(subreddits.get_new(limit=50))
    for submission in hot_submissions:
        if submission.id not in processed and 'imgur.com' not in submission.url and 'flickr.com' not in submission.url and 'livememe.com' not in submission.url:
            try:
                rehost_url = imgur_rehost_image(submission.url, submission.title)
                comment = "[Imgur mirror](%s), in case the original would go down.\n\n(Yes, I'm a bot. See my code [here](https://github.com/BramBonne/reddit_rehosting_bot).)" % rehost_url
                submission.add_comment(comment)
                print "Replied to submission %s" % submission.title
                commented_on.add(submission.id)
            except HTTPError:
                print "%s was not an image" % submission.url
            except praw.errors.RateLimitExceeded as e:
                print "\rComment rate limit temporarily exceeded (%s), deferring until next round." % e.message
                sleep(60) # Prevent reddit from penalizing us
                continue # Handle next item in the list
        processed.add(submission.id)
    sleep(2)
    round += 1