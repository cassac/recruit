from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django_countries.fields import CountryField

class BaseUser(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True)
	first_name = models.CharField(max_length=50, blank=False)
	last_name = models.CharField(max_length=50, blank=False)
	citizenship = CountryField(blank=False)
	timezone = models.CharField(max_length=50, blank=False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

class Candidate(BaseUser):
	date_of_birth = models.DateField(blank=True)
	education = models.CharField(
			max_length=25,
			blank=True,
			choices=(
			('High School','High School'),
			('Vocational School', 'Vocational School'),
			('Community College','Community College'),
			("Bachelor's Degree", "Bachelor's Degree"),
			("Master's Degree", "Master's Degree"),
			('MBA', 'MBA'),
			('PhD', 'PhD'),						
		)
	)	
	education_major = models.CharField(max_length=250, blank=True)
	current_location = CountryField(blank=True)	
	USERNAME_FIELD = 'pk'

	def __str__(self):
		return self.email