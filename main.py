import webapp2
from api.base import BaseHandler
from api import user_service, tweet_service



class HomeHandler(BaseHandler):
    def get(self):
        self.redirect('/app')



#ERROR HANDLERS

def handle_404(request, response, exception):
    response.write('Oops! I could swear this page was here! <a href="/">go back</a>')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('A server error occurred!')
    response.set_status(500)


config = {
  'webapp2_extras.sessions': {
    'secret_key': 'muvedo-is-art-09-2007',
    'cookie_args':{'max_age':31622400}
  }
}

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/access/passport', user_service.AccessPassportHandler),
    ('/access/request', user_service.AccessRequestHandler),
    ('/access/verify', user_service.AccessVerifyHandler),
    ('/service/tweet/create', tweet_service.CreateTweet),
    ('/service/tweet/my', tweet_service.MyTweets),
    ('/service/tweet/feed', tweet_service.Feed),
    ('/service/tweet/communityfeed', tweet_service.CommunityFeed),
    ('/service/tweet/person', tweet_service.Person),
    ('/service/tweet/follow', tweet_service.Follow)

], debug=True, config=config)


app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500