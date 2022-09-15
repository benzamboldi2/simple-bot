import tweepy
import config
import datetime

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("We are all set, let's get started...")
except:
    print("Uh oh... we ran into a problem authenticating")
    raise BrokenPipeError("Authentication pipe is leaky")

now = datetime.datetime.now()
firstTweet = "Happy Birthday to Simple Bot! " + str(now) + " EST is Simple Bot's exact moment of inception. BZ"

api.update_status(firstTweet)