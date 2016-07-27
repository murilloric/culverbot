import logging
import urllib
import webapp2
import json
import os
from webapp2_extras import sessions
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from api.base import BaseHandler
from api import hooks
from api.models import UserModel
from api.models import UserStore



#DEFS
IS_TEST = True
if IS_TEST:
    AUTHY_KEY = '7ea6e01f516b0a3ba8e9df75d1f9a6f6'
    AUTHY_HOST = 'http://sandbox-api.authy.com'
else:
    AUTHY_KEY = 'fqDE0tQy22UVsT1eyO38erVdnzeSA4bL'
    AUTHY_HOST = 'https://api.authy.com/'

def tempUserSession(self):
    cookie = self.session_store.get_session()
    try:
        cookie = self.session_store.get_session(name='ricsmasterapp-cookie')
        session = cookie['ricsmasterapp-temp-access-control']
        return session
    except:
        return False

def clearUserSession(self):
    cookie = self.session_store.get_session()
    try:
        cookie = self.session_store.get_session(name='ricsmasterapp-cookie')
        del self.session['ricsmasterapp-valid-access-control']
        return True
    except:
        return False

def CallAuthy(url, idx, data):
    calls = [urlfetch.POST, urlfetch.GET, urlfetch.GET]
    networkCall = urlfetch.fetch(url=url,
        payload=json.dumps(data),
        method= calls[idx],
        headers={'Content-Type': 'application/json'})
    return networkCall

#DEFS


#HANDLERS

class AccessPassportHandler(BaseHandler):
	@hooks.oAuthUserRequired
	def get(self, authy_id, user):
		if authy_id:
			logging.info(user)
			BaseHandler.server_resp(self, 200, 'Valid Passport', user)
		else:
			BaseHandler.server_resp(self, 401, 'Not logged in', {})

class AccessRequestHandler(BaseHandler):
    def post(self):
        data = json.loads(self.request.body)
        email = data['email']
        cellphone = data['cellphone']
        reg_url = AUTHY_HOST + "/protected/json/users/new?api_key="+AUTHY_KEY
        reg_payload = {
            "user": {
                "email": email,
                "cellphone": cellphone,
                "country_code": "1"
            }
        }
        result = CallAuthy(reg_url, 0, reg_payload)
        resp = json.loads(result.content)
        if resp['success'] == True:
            authy_id = str(resp['user']['id'])
            self.session['ricsmasterapp-temp-access-control'] = {'authy_id':authy_id, 'email':email, 'cellphone':cellphone}
            sms_url = AUTHY_HOST + "/protected/json/sms/" + authy_id + "?api_key="+AUTHY_KEY
            sms_payload = {
                    "user": {
                        "via": "sms",
                        "phone_number": cellphone,
                        "country_code": "1",
                        "locale":"en"
                    }
                }
            sms_result = CallAuthy(sms_url, 1, sms_payload)
            sms_resp = json.loads(sms_result.content)
            if sms_resp['success'] == True:
                BaseHandler.server_resp(self, 200, 'Text Message Sent' , sms_resp)
        else:
            self.response.set_status(401)
            BaseHandler.server_resp(self, 401, 'we could not register your account', resp)

class AccessVerifyHandler(BaseHandler):
    def post(self):
        temp_session = tempUserSession(self)
        try:
            authy_id = temp_session['authy_id']
            email = temp_session['email']
            cellphone = temp_session['cellphone']
            data = json.loads(self.request.body)
            token = data['access_token']
            verify_url = AUTHY_HOST + "/protected/json/verify/" + token + '/' + authy_id + "?api_key="+AUTHY_KEY
            data = {}
            authy_resl = CallAuthy(verify_url, 1, data)
            authy_resp = json.loads(authy_resl.content)
            if authy_resp['token'] == 'is valid':
                del self.session['ricsmasterapp-temp-access-control']
                self.session['ricsmasterapp-valid-access-control'] = authy_id
                user = UserStore(authy_id, email, cellphone).newUserEntity()
                BaseHandler.server_resp(self, 200, 'Access Granted', user)
            else:
                del self.session['ricsmasterapp-temp-access-control']
                self.response.set_status(401)
                BaseHandler.server_resp(self, 401, 'Invalid Token', {})
        except Exception as e:
            logging.info(e)
            self.response.set_status(401)
            BaseHandler.server_resp(self, 401, 'Expired Token', {})

#HANDLERS