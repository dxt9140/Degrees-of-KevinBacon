"""
kb.py
Author: Dominick Taylor (dxt9140@g.rit.edu)
Contributor: Christopher Homan
Created: 2/2/2018
Find the "Bacon Number" for a specified user account using a series
of tweets to connect the two.
"""

from twython import Twython

# My files
import header as h
import pq

# Sys files
import json
import sys
import pprint as pp
import codecs
import time
import threading

# Make strings prettier
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

twitter =  Twython(h.consumer_key, h.consumer_secret,
                    h.access_token, h.access_token_secret)

# Construct an instance of twitter
# twitter = Twython(h.consumer_key, h.access_token=ACCESS_TOKEN)

"""
Class to encapsulate the relevant data for a tweet.
"""
class TweetNode:
	# The sequence of tweets leading up to this one.
	sequence = None

	# The handle of the user who made this tweet.
	handle = None

	# The text of the tweet. Encoded in UTF-8.
	text = None

	# A list of the mentions contained within this tweet.
	mentions = None

	# The twitter ID number of this tweet.
	twid = None

	# The only value not grabbed from the tweet metadata. This value is
	# set when initializing the tweet. It is used to place a priority 
	# on the tweet.
	value = None
	
	def __init__(self, handle, text, mentions, twid, previous):
		self.handle = handle
		self.text = text
		self.mentions = mentions
		self.twid = twid
		if previous == None:
			self.sequence = list()
			self.sequence.append( self )
		else:
			self.sequence = list( previous.sequence )
			self.sequence.append( self )
		self.value = 0


	# Determine if a tweet is the goal state.
	def goalTest( self ):
		if self.handle == h.TARGET_ACCOUNT:
			return True
		elif h.TARGET_ACCOUNT in self.text:
			return True
		elif "Kevin Bacon" in self.text:
			return True
		elif "kevin bacon" in self.text:
			return True
		elif "KevinBacon" in self.text:
			return True
		elif "kevinbacon" in self.text:
			return True
		elif "@KevinBacon" in self.text:
			return True
		else:
			return False

"""
Tweet a node in a way that displays Unicode characters.
"""
def uprint( node ):
	handle = node.handle + " "
	text = node.text
	unitext = text.encode('utf8').decode('utf8')
	string = handle + str(node.twid) + " " + unitext
 	print( string )


"""
Given a node, determine its arbitrary value.
"""
def scanTweets( node ):
	text = node.text

	evaluation = 0

	"""
	Unique mentions are valuable, but too many can cause us to get lost in a
	circle of tweets that looks like "@JOHN @BillyBob @KEvinSmith @CatBrowser10
	@Everybody..." etc.
	"""
	for mention in node.mentions:
		if mention not in h.already_seen_mentions:
			evaluation += 1

	# Scan the text for valuable keywords
	words = text.split()
	for word in words:
		if word in h.valuable_words:
			# This metric is not super powerful but I chose to leave it
			# in. Valuable keywords are rare for Kevin Bacon (because he
			# doesn't tweet much), but may be more useful for active users.
			evaluation += (2 * h.valuable_words[word])
		elif word in h.valuable_hashtags:
			# If a tweet contains a hashtag that the target account has
			# tweeted about, this tweet is very valuable.
			evaluation += 10

	# Add an absurd value of the goal state is found.
	if node.goalTest():
		evaluation += 1000000

	# Tweets that have already been expanded are not valuable
	if node.twid in h.already_seen_tweets:
		evaluation = 0

	node.value = evaluation


"""
Place a query on a given handle.
"""
def placeQuery( handle, consider ):

	tweets = list()
	
	# As soon as a handle has been queried, mark it as seen
	h.already_seen_mentions.add( handle )

	query = "from:%s" % handle
	search = twitter.search( q=query, count=20, tweet_mode='extended' )
	results = search['statuses']

	for this_tweet in results:
		mentions = list()
		user_mentions = this_tweet['entities']['user_mentions']
		# Grab the mentions within the tweet.
		for mention in user_mentions:
			account = mention['screen_name']
			username = "@" + str(account)
			mentions.append( username )
		text = this_tweet['full_text']
		node = TweetNode( handle, text, mentions, this_tweet['id'], consider )
		scanTweets( node )
		if node.value > 0:
			# If a tweet has value, mark it as seen and include it
			# in future searches
			h.already_seen_tweets.add( node.twid )
			tweets.append( node )
		else:
			del node

	return tweets


"""
Grab tweets to examine and expand.
"""
def handlePercepts():
	tweet_queue = pq.PQ()
	
	initial_set = placeQuery( sys.argv[1], None )

	for tweet in initial_set:
		tweet_queue.insert( tweet )

	while 1:
		consider = tweet_queue.pop()
		# uprint( consider )
		if consider.goalTest() is True:
			return consider.sequence
		else:
			for mention in consider.mentions:
				tweets = placeQuery( mention, consider )
				for tweet in tweets:
					tweet_queue.insert( tweet )
					
				time.sleep( 3 )	

def main():
	# Allows specification of a target account that is not Kevin Bacon.
	if len(sys.argv) == 3:
		h.TARGET_ACCOUNT = sys.argv[2]

	# Grab some of the keywords and hashtags relevant to the target account.	
	h.preprocess( twitter )

	print("Running...")
	# Begin execution by looking at queries.
	sequence = handlePercepts()

	# Print the found sequence of tweets
	print; print
	for tweet in sequence:
		uprint( tweet )
 
	
if __name__ == '__main__': 
    main()

# End of File

