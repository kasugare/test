#!/usr/bin/python
# -*- coding : utf-8 -*-

from functools import wraps

def is_admin(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if kwargs.get('username') != 'admin':
			raise Exception("permisstion denied!")
		return func(*args, **kwargs)
	return wrapper

class Greet(object):
	current_user = None

	@is_admin
	def set_name(self, username):
		self.current_user = username

	@is_admin
	def get_greeting(self, username):
		# print "username : {}".format(username)
		return "Hello {}".format(self.current_user)


greet = Greet()
print dir(greet)
greet.set_name(username='admin')
print ' -', greet.get_greeting(username='admin')
print ' - __name__ : ', greet.get_greeting.__name__
print ' - __doc__ :', greet.get_greeting.__doc__

print dir(wraps)