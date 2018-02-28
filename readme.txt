Degrees of @KevinBacon
Author: Dominick Taylor

Introduction

2/27/2018
The program in its current form will be labeled v1.0. I would love to improve
this project in the future, but for the current use, it will do. It uses an
array heap to and some arbitrary evaluation methods to ensure that the most
"valuable" tweet will be examined next. This is an example of a Best-First
Search. This has its issues which will be further discussed in the 
Overview.pdf document. 

Execution:

	$> python kb.py <user>
	$> python kb.py <start_user> <target_user>

	In each case, the first argument should be the user to begin a search
	from. 
	In the second command execution, target_user can be used to specify a
	different user to search for. Default is @KevinBacon. 

	Note: In all cases, specifying a user MUST begin with the @symbol,
	otherwise the Twitter API will return an error.

Example:

	The file test1.txt contains a simple example using the command:

	$> python2 kb.py @CNN @realDonaldTrump

	It serves as a proof of concept. CNN tweeted @POTUS, who tweeted
	@realDonaldTrump. The output follows the form of:

	USER_NAME TWEET_ID TWEET

Future Improvements:

	> Error checking for input
	> Better search algorithmn. Best-First search does not have enough data
	  to provide a decent evaluation.
	> Better evaluation function if this algorithm is kept.
		- Verified users are more valuable
		- Peruse followers to find potential links


