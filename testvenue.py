import os
import sys
import logging
sys.path.insert(1, '/usr/local/google_appengine')
sys.path.insert(1, '/usr/local/google_appengine/lib/yaml/lib')
import webapp2
from google.appengine.ext import testbed
import unittest
import webtest
from api import venue_service


class AppTest(unittest.TestCase):
    def setUp(self):
        config = {
          'webapp2_extras.sessions': {
            'secret_key': 'muvedo-is-art-09-2007',
            'cookie_args':{'max_age':31622400}
          }
        }
        app = webapp2.WSGIApplication([
            ('/venue/create', venue_service.PostVenueHandler)
            ],debug=True, config=config)
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def testHelloWorldHandler(self):
        cookie_args = {'ricsmasterapp-cookie':'eyJyaWNzbWFzdGVyYXBwLXZhbGlkLWFjY2Vzcy1jb250cm9sIjoiNDIzNjU1In0\075|1456032518|c425870d864ed9bfda5fa057910b017b9f9bc247'}
        response = self.testapp.get('/venue/create', headers=cookie_args)
        print (response)
        self.assertEqual(response.status_int, 200)
        #self.assertEqual(response.normal_body, 'Hello World!')
        #self.assertEqual(response.content_type, 'text/plain')


if __name__ == '__main__':
    unittest.main()