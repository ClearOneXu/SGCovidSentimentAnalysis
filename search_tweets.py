import tweepy
import json

# consumer_key = 'LdNoze6jRzqgk4EIA3oTPRKEy'
# consumer_secret = 'hl6pH1romVqDEyVoNeGSMGe1XfuHhWR8IXYXScN2R76MGhnoAZ'
# access_token = '1229011293446606848-AEV7ziKGpv59L3PGJeJlbQRpD5oMb0'
# access_token_secret = 'vm9g5excYmT41UblTq0nIXwnpnj9ItMWJpU5D0IYw3q6p'

# consumer_key = 'J81uFNDREsco9Wfi6TFcIAioc'
# consumer_secret = '1JP88VJxiby0yPimcrx9rCUHL08EOL9B5HAncWxWRIKA70WSCA'
# access_token = '1229017825370492930-H7mie8Bh8qQP3yG5xEtBBv3HFBAGAW'
# access_token_secret = 'QmxI50MP7DGOZ5cd1TGhl0JLrthPopHmW6q7h7W1EOZff'

consumer_key = 'sUScSVIjrgUd5cO96QjAPHz5G'
consumer_secret = 'zrfgZX8Kig4uodBEH7BfRYFa1Xj81ZTOLylczo1utXWjDW6Uls'
access_token = '1217112496491749376-buFH3a4MADn0570uexCEetJAcdLAZa'
access_token_secret = 'XaeyAgs3ppsgnjsSKG09Rj4fCcBqXlNknefO2mtAX8ko3'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if __name__ == '__main__':
    for i in range(1):
        query = 'geocode:1.31,103.83,30km covid19 OR covid OR coronavirus OR covid-19 lang:en since:2020-03-23 until:2020-03-24'

        cricTweet = tweepy.Cursor(api.search, q=query,tweet_mode='extended', retweeted_status='full_text', result_type='recent',count=1000).items(50000)
        with open('data/covid_0323_0' + '.json', 'a', encoding='utf-8') as fp:
            for tweet in cricTweet:
                fp.write(json.dumps(tweet._json))
                fp.write('\r')
