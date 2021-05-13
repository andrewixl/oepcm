from __future__ import unicode_literals
# from ..portal.models import Course
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registerVal(self, postData):
		results = {'status': True, 'errors': [], 'user': None}
		if len(postData['firstName']) < 3:
			results['status'] = False
			results['errors'].append('First Name must be at least 3 characters - Account Not Created')
		if len(postData['lastName']) < 3:
			results['status'] = False
			results['errors'].append('Last Name must be at least 3 characters - Account Not Created')
		if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
			results['status'] = False
			results['errors'].append('Email entered is invalid  - Account Not Created')
		if len(postData['password']) < 4  or  postData['password'] != postData['c_password']:
			results['status'] = False
			results['errors'].append('Password is too short  - Account Not Created')
		if postData['password'] != postData['c_password']:
			results['status'] = False
			results['errors'].append('Passwords do not Match  - Account Not Created')

		user = User.objects.filter(email = postData['email'])
		print (user, '*****', len(user))
		if len(user) >= 1:
			results['status'] = False
			results['errors'].append('User already exists - Account Not Created')

		#check to see if user is not in db
		return results
	def createUser(self, postData):
		p_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

		user = User.objects.create(
			active = True, 
			firstName = postData['firstName'], 
			lastName = postData['lastName'], 
			email = postData['email'], 
			emailVerified = False, 
			password = p_hash,)
		return user

	# Used to check if user entered correct email and password	
	def loginVal(self, postData):
		results = {'status': True, 'errors': [], 'user': None}
		results['user'] = User.objects.filter(email = postData['email'])
		if len(results['user'] ) <1:
			results['status'] = False
			results['errors'].append('User does not exist')
		else:
			hashed = bcrypt.hashpw(postData['password'].encode(), results['user'][0].password.encode())
			if hashed  != results['user'][0].password:
				results['status'] = False
				results['errors'].append('Something went wrong')
		return results


profile_default = '/media/profileplaceholder.png'

class User(models.Model):
	active = models.BooleanField(verbose_name='Active?')
	PERMISSION = (
        ('administrator', "Administrator"),
        ('standard', "Standard"),
    )
	permission = models.CharField(max_length=20, choices=PERMISSION, verbose_name='Permission')
	firstName = models.CharField(verbose_name='First Name', max_length = 20)
	lastName = models.CharField(verbose_name='Last Name', max_length = 20)
	email = models.CharField(verbose_name='Email Address', max_length = 40)
	emailVerified = models.BooleanField(verbose_name='Email Verified?')
	password = models.CharField(verbose_name='Password', max_length = 1000)
	# profile_photo = models.ImageField(upload_to="media/", default='media/placeholder-profile-1.png')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __str__(self):
		return self.firstName + " " + self.lastName