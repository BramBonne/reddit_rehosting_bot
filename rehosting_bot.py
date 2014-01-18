__author__ = 'bram'

import praw
import pyimgur
from requests.exceptions import HTTPError
from time import sleep

IMGUR_API_KEY = ""
REDDIT_USERNAME = ""
REDDIT_PASSWORD = ""

SUBREDDITS = 'pics+images+gifs+reactiongifs+AdviceAnimals+mildlyinteresting+aww+funny'
EXCLUDED_DOMAINS =  ['imgur.com', 'flickr.com', 'livememe.com', 'tumblr.com']


api = praw.Reddit('A bot rehosting images on imgur.com by /u/gooz and /u/piratenaapje')
api.login(REDDIT_USERNAME, REDDIT_PASSWORD)
imgur_api = pyimgur.Imgur(IMGUR_API_KEY)
subreddits = api.get_subreddit(SUBREDDITS)
processed = set()
commented_on = set()
round = 1
while True:
    print "\rRound %d: commented %d times" % (round, len(commented_on)),
    hot_submissions = set(subreddits.get_new(limit=50))
    for submission in hot_submissions:
        if submission.id not in processed and not any(domain in submission.url for domain in EXCLUDED_DOMAINS):
            try:
                rehost_url = imgur_api.upload_image(url=submission.url, title=submission.title).link
                comment = "[Imgur mirror](%s), in case the original would go down.\n\n" % rehost_url
                comment += "(Yes, I'm a bot. See my code "
                comment += "[here](https://github.com/BramBonne/reddit_rehosting_bot).)"
                submission.add_comment(comment)
                print "\nReplied to submission %s" % submission.title
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