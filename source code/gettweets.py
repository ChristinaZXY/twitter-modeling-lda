#!/usr/bin/python
from urlparse import urlparse
from twitter import *
import csv
# uses the python twitter package found at https://github.com/sixohsix/twitter

# initialize some variables
topics = ['apple', 'microsoft', 'google', 'amazon']
tweets = []

# initialize twitter instance
CONSUMER_KEY, CONSUMER_SECRET = read_token_file(".app_auth")
oauth_token, oauth_secret = read_token_file(".my_auth")
tstream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

# get tweets
for topic in topics:
    iterator = tstream.statuses.filter(language='en', track=topic)
    count = 0
    print "Getting tweets for topic: " + topic + " ..."
    
    for tweet in iterator:
        if count >= 100:
            break
        
        if not tweet["retweeted"]:  #filter out retweets
            text = tweet['text'].replace('\n', ' ')
            
            words = text.split()    #remove URLs
            for i in range(len(words)):
                r = urlparse(words[i])
                if r[0] != '' and r[1] != '':
                    words[i] = ""
                    
            text = ' '.join(words).encode('utf-8')
            tweets.append( [topic, '?', tweet['id_str'], 'DC', text] )
            count += 1

# write tweets to file
print "Writing all tweets to file ... "
tfile = open('tweets.csv', 'wb')
writer = csv.writer(tfile, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
for tweet in tweets:
    writer.writerow(tweet)
print "Done!"