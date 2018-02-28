"""
header.py
Author: Dominick Taylor (dxt9140@g.rit.edu)
Created: 2/11/2018
File used to store constant structures and helper functions. Used to
cleanup kb.py.
"""

import unicodedata

# Define the target account. Used for testing primarily. Default is Kevin
# Bacon.
TARGET_ACCOUNT = '@KevinBacon'

# enter your keys, and tokens obtained from your twitter app
consumer_key="M9DkwDR6NLWGCe8lFKJr8U7KI"
consumer_secret="hNvWeWS4zdy0o4lAcBWUAPG8LcS1Ovr8iD4WNdBz5S51hGARCX"
access_token="85429056-cn10mxq3dCXyrEe2NUg9BE8Djs4LDNeS04gm6q8A2"
access_token_secret="Ou2y55wygF5UBW6OSukO6NS4NedxrobZVGwJf33WzQjcW"

# oauth2 token for better query rate. Better than oauth1 because this is
# read only, whereas oauth1 has write access.
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAALwv4QAAAAAAoBlY2e5YrvqY0xeHlT2OQhqjAJc%3DfkRIGsZTzbQ2R3mst8hHd3ExBXs57qosejdHInkw7VQvsEGRzz'

"""
Set containing words to ignore when creating valuable_words dictionary.
"""
blacklist = {'at', 'to', 'this', 'that', 'them', 'those', 'they', 'he', 'she', 
	'it', 'and', 'the', 'a', 'an', 'here', 'there', 'their', 'they\'re', 
	'be', 'by', 'I', 'have', 'had', 'theyre', 'what', 'where', 'when', 'was',
	'for', 'too', 'and', 'don\'t', 'dont', 'of', 'have' 'had', 'Im', 'me',
	'The', 'my', 'are', 'We', 'it.', 'do', 'And', 'My' }

"""
Words used to evaluate tweets based on the target account's recent tweets.
"""
valuable_words = dict()

"""
Hashtags that the target account has been tweeting about.
"""
valuable_hashtags = set()

"""
Tweet ids of tweets that have already been expanded. 
"""
already_seen_tweets = set()

"""
Set containing handles of users that have already been queried.
"""
already_seen_mentions = set()

"""
Place a query on the target account. Gather keywords, hashtags, and mentions
from the target account's tweets. This is used to evaluate tweets when looking for a path.
"""
def preprocess( twitter ):

	query = "from:%s" % TARGET_ACCOUNT
	search = twitter.search( q=query, count=20, tweet_mode='extended' )
	results = search['statuses']

	for tweet in results:
		text = tweet['full_text']
		words = text.split()
		for uniword in words:
			word = uniword.encode('utf8', 'replace')
			if word not in blacklist and word != '':
				if word[0] is '#':
					if word not in valuable_hashtags:
						valuable_hashtags.add( word )
				else:
					if word not in valuable_words:
						valuable_words[word] = 1
					else:
						valuable_words[word] += 1
	
