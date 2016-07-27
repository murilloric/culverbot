import logging
import urllib
import webapp2
import json
import os
from webapp2_extras import sessions
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import time
import datetime

from api import hooks
from api.base import BaseHandler
from api.models import UserModel


#MODELS

class TweetModel(ndb.Model):
    authy_id = ndb.StringProperty()
    tweet = ndb.TextProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)


class FollowModel(ndb.Model):
    authy_id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    is_following = ndb.BooleanProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)

#MODELS

#HANDLERS


def isFollowing(authy_id, person_authy_id):
	following = FollowModel.query(FollowModel.authy_id == authy_id, FollowModel.user_id == person_authy_id).get()
	logging.info(following)
	is_following = False
	if(following == None):
		FollowModel(authy_id=authy_id, user_id=person_authy_id, is_following=False).put()
	else:
		is_following = following.is_following
	return is_following

class Follow(BaseHandler):
	@hooks.oAuthUserRequired
	def post(self, authy_id, user):
		if authy_id:
			user_name = json.loads(self.request.body)
			follow_user = UserModel.query(UserModel.user_name == user_name['user_name']).get()
			user_id = follow_user.authy_id
			following = FollowModel.query(FollowModel.authy_id == authy_id, FollowModel.user_id == user_id).get()
			logging.info(following)
			if(following == None):
				FollowModel(authy_id=authy_id, user_id=user_id, is_following=True).put()
			else:
				if(following.is_following):
					following.is_following = False
				else:
					following.is_following = True

				following.put()
			
			BaseHandler.server_resp(self, 200, 'Follow a Person', {})
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})

class Person(BaseHandler):
	@hooks.oAuthUserRequired
	def post(self, authy_id, user):
		if authy_id:
			person_req = json.loads(self.request.body)
			person = UserModel.query(UserModel.user_name == person_req['user_name']).get()
			tweets = TweetModel.query(TweetModel.authy_id == person.authy_id).order(-TweetModel.date_created).fetch(20)
			person_tweets = []
			for t in tweets:
				person_tweets.append(
					{'date_created':t.date_created.strftime('%m/%d/%Y') ,
					'tweet':t.tweet}
				)

			is_following = isFollowing(authy_id, person.authy_id);

			person_data = {'user_name':person.user_name, 'following': is_following, 'tweets':person_tweets}

			BaseHandler.server_resp(self, 200, 'My Tweets', person_data)
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})

class Feed(BaseHandler):
	@hooks.oAuthUserRequired
	def get(self, authy_id, user):
		if authy_id:
			logging.info(user['user_name'])
			my_feed = []
			feed = UserModel.query().fetch(10)
			for f in feed:
				if f.user_name != user['user_name']:
					logging.info(f)
					recent_tweet = TweetModel.query(TweetModel.authy_id == f.authy_id).get()
					is_following = isFollowing(authy_id, f.authy_id)
					if is_following:
						my_feed.append({'user_name':f.user_name, 'following': is_following, 
										'tweet':recent_tweet.tweet, 'date_created':recent_tweet.date_created.strftime('%m/%d/%Y')})
			BaseHandler.server_resp(self, 200, 'My Tweets', my_feed)
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})

class CommunityFeed(BaseHandler):
	@hooks.oAuthUserRequired
	def get(self, authy_id, user):
		if authy_id:
			logging.info(user['user_name'])
			my_feed = []
			feed = UserModel.query().fetch(10)
			for f in feed:
				if f.user_name != user['user_name']:
					logging.info(f)
					recent_tweet = TweetModel.query(TweetModel.authy_id == f.authy_id).get()
					is_following = isFollowing(authy_id, f.authy_id)
					my_feed.append({'user_name':f.user_name, 'following': is_following, 
						'tweet':recent_tweet.tweet, 'date_created':recent_tweet.date_created.strftime('%m/%d/%Y')})
			BaseHandler.server_resp(self, 200, 'My Tweets', my_feed)
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})




class MyTweets(BaseHandler):
	@hooks.oAuthUserRequired
	def get(self, authy_id, user):
		if authy_id:
			logging.info(user)
			my_tweets = []
			tweets = TweetModel.query(TweetModel.authy_id == authy_id).order(-TweetModel.date_created).fetch(5)
			for t in tweets:
				my_tweets.append(
					{'date_created':t.date_created.strftime('%m/%d/%Y') ,
					'tweet':t.tweet}
				)
			logging.info(my_tweets)
			BaseHandler.server_resp(self, 200, 'My Tweets', my_tweets)
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})

class CreateTweet(BaseHandler):

	@hooks.oAuthUserRequired
	def post(self, authy_id, user):
		if authy_id:
			tweet_data = json.loads(self.request.body)
			logging.info(tweet_data)

			TweetModel(
				authy_id = authy_id,
				tweet = tweet_data['message']
			).put()

			BaseHandler.server_resp(self, 200, 'Tweet Created', {})
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})



#HANDLERS
