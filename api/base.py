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


#HANDLERS
class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(name='ricsmasterapp-cookie', max_age=3600, factory=None,
                    backend='securecookie')

    def server_resp(self, status, message, data):
        message = json.dumps({'status':status, 'message':message, 'data':data})
        self.response.write(message)

