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
	
