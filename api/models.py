import logging
from google.appengine.ext import ndb

class UserModel(ndb.Model):
    authy_id = ndb.StringProperty()
    access_date = ndb.DateTimeProperty(auto_now_add=True)
    user_name = ndb.StringProperty()
    email = ndb.StringProperty()
    cellphone = ndb.StringProperty()
    role = ndb.StringProperty()
    


class UserStore(object):
	def __init__(self, authy_id, email, cellphone):
		self.authy_id = authy_id
		self.user = 'Ric'
		self.email = email		
		self.cellphone = cellphone

	def getUserEntity(self):
		userObject = UserModel.query(UserModel.authy_id == self.authy_id).get()
		if userObject:
			return userObject
		else:
			return False

	def newUserEntity(self):
		user_name = self.email.split('@')
		userObj = UserModel.get_or_insert(str(self.authy_id), authy_id=self.authy_id, user_name=user_name[0], email=self.email, cellphone=self.cellphone)
		user = userObj.to_dict(exclude=['access_date', 'authy_id'])
		return user
