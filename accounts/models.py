import pytz

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django_countries.fields import CountryField
from django.utils import timezone

TIMEZONE_CHOICES = tuple((choice, choice) for choice in pytz.common_timezones)

class BaseUser(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True)
	first_name = models.CharField(max_length=50, blank=False)
	last_name = models.CharField(max_length=50, blank=False)
	gender = models.CharField(max_length=10, blank=True, choices=(('male','male'),('female', 'female'),))
	citizenship = CountryField(blank=False)
	timezone = models.CharField(
			max_length=50, 
			blank=False,
			choices=TIMEZONE_CHOICES,
		)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)


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
	available = models.DateField()
	USERNAME_FIELD = 'pk'

	def __str__(self):
		return self.email

class CandidatePreferencesLocation(models.Model):
	country = CountryField(blank=True)

	def __str__(self):
		return self.country

class CandidatePreferencesEmployerType(models.Model):
	employer_type = models.CharField(
		max_length=100,
		choices=(
			('University', 'University'), 
			('High School', 'High School'),
			('Middle School', 'Middle School'), 
			('Primary School', 'Primary School'),
			('Kindergarten', 'Kindergarten'),
			('Youth Language Center', 'Youth Language Center'),
			('Adult Language Center', 'Adult Language Center'),			
		)
	)
	def __str__(self):
		return self.employer_type

class CandidatePreferencesPositionType(models.Model):
	job_title = models.CharField(
		max_length=10,
		choices=(
			('Teacher', 'Teacher'), 
			('Manager', 'Manager'),
			('Partner', 'Partner'), 									
		)
	)
	def __str__(self):
		return self.job_title				

class CandidatePreferences(models.Model):
	candidate = models.OneToOneField(
		Candidate,
		on_delete=models.CASCADE,
	)
	location = models.ManyToManyField(CandidatePreferencesLocation, blank=True)
	employer_type = models.ManyToManyField(CandidatePreferencesEmployerType, blank=True)
	desired_job_title = models.ManyToManyField(CandidatePreferencesPositionType, blank=True)
	desired_monthlty_salary = models.CharField(
		blank=True,
		max_length=10,
		choices=(
			('1000', '1000+'), 
			('2000', '2000+'), 
			('3000', '3000+'),
			('4000', '4000+'), 
			('5000', '5000+'),
			('6000', '6000+'), 
			('7000', '7000+'),
			('8000', '8000+'), 
			('9000', '9000+'),
			('10000', '10000+'),
			('11000', '11000+'), 
			('12000', '12000+'),
			('13000', '13000+'),
			('14000', '14000+'),
			('15000', '15000+'), 
			('16000', '16000+'),
			('17000', '17000+'),
			('18000', '18000+'),
			('19000', '19000+'),
			('20000', '20000+'),
			('21000', '21000+'),
			('22000', '22000+'),
			('23000', '23000+'),
			('24000', '24000+'),
			('25000', '25000+'),								 
		)
	)

	def __str__(self):
		return self.candidate.email