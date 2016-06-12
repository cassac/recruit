from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from django.core import signing
from django.core.signing import SignatureExpired, BadSignature

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from allauth.account.models import EmailAddress

from jobs.models import Job

from recruit.choices import (TIMEZONE_CHOICES, COUNTRY_CHOICES, GENDER_CHOICES,
	EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES, POSITION_TYPE_CHOICES, 
	DESIRED_MONTHLY_SALARY_CHOICES)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	timezone = models.CharField(choices=TIMEZONE_CHOICES, max_length=50, blank=True)
	citizenship = CountryField(blank_label='(Select country)')
	skype_id = models.CharField(max_length=50, blank=True)
	user_type = models.CharField(
		choices = (('Candidate', 'Candidate'), ('Recruiter', 'Recruiter'), ('Employer', 'Employer'),),
		max_length = 50,
	)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.user.email

	def generate_token(self):
		email = self.user.email
		token = signing.dumps({'email': email})
		return token

	@staticmethod
	def verify_token(token, max_age=604800):
		# default max_age is 7 days
		try:
			value = signing.loads(token, max_age=max_age)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user = User.objects.get(email=value['email'])
		return user

def create_account_emailaddress(sender, instance, created, **kwargs):
	# Used for django-allauth
	if created:
		EmailAddress.objects.get_or_create(
			user_id=instance.id,
			email=instance.email
		)
post_save.connect(create_account_emailaddress, sender=User)