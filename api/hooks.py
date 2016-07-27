import logging

from api.models import UserStore
from api.base import BaseHandler

def oAuthUserRequired(handler_method):
    def checkUser(self):
        cookie = self.session_store.get_session()
        logging.info(cookie)
        try:
            cookie = self.session_store.get_session(name='ricsmasterapp-cookie')
            authy_id= str(cookie['ricsmasterapp-valid-access-control'])
            us = UserStore(authy_id, 'None', 'None')
            userObj = us.getUserEntity()
            user = userObj.to_dict(exclude=['access_date', 'authy_id'])
            handler_method(self, authy_id, user)
        except Exception as e:
            logging.info(e)
            self.response.set_status(401)
            BaseHandler.server_resp(self, 401, 'Not authorized to use Rics Master App', {})
    return checkUser