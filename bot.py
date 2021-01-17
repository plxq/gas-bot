import time
import requests
from tweepy  import OAuthHandler, API

# A local file with twitter credentials
import keys

Auth = OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
Auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_SECRET)
TwitterBot = API(Auth)

def tweet_send(msg):
    TwitterBot.update_status(msg)

def tweet_format(json):
    msg = """[Block No. {0}]

Slow: {1} gwei
Average: {2} gwei
Fast: {3} gwei

Go mint your shit :)
""".format(json["blockNum"], 
           int(json["safeLow"])/10, 
           int(json["average"])/10, 
           int(json["fast"])/10)

    return msg

def gas_price_delayed(sleep):
    print("Sleeping for {0} seconds...".format(sleep))
    time.sleep(sleep)
    sleep = sleep*2
    gas_price(sleep)

def gas_price(sleep=60):
    try:
        url = "https://ethgasstation.info/api/ethgasAPI.json"
        response = requests.get(url, timeout=3)
        data = response.json()
        return data
    except Exception as e:
        print(e)
        gas_price_delayed(sleep)

def unix_now():
    return round(time.time())

class Bot:
    def __init__(self):
        self.last = 0
        self.wait = 5*60 # Check every 5 minutes
        self.threshold = 25 # Gwei threshold
        self.delay = 24*60*60 # Only every 24 hours

    def check(self):
        json = gas_price()
        gwei = int(json["average"])/10
        if gwei < self.threshold:
            if unix_now()-self.last >= self.delay:
                msg = tweet_format(json)
                print(unix_now())
                print(msg)
                tweet_send(msg)
                self.last = unix_now()

    def start(self):
        while True:
            self.check()
            time.sleep(self.wait)

b = Bot()
b.start()
