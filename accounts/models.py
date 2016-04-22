from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from .choices import (TIMEZONE_CHOICES, COUNTRY_CHOICES, GENDER_CHOICES,
	EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES, POSITION_TYPE_CHOICES, 
	DESIRED_MONTHLY_SALARY_CHOICES)

class BaseUser(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True)
	first_name = models.CharField(max_length=50, blank=False)
	last_name = models.CharField(max_length=50, blank=False)
	gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
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
			choices=EDUCATION_CHOICES,
		)	
	education_major = models.CharField(max_length=250, blank=True)
	current_location = CountryField(blank=True)
	available = models.DateField()
	USERNAME_FIELD = 'pk'

	def __str__(self):
		return self.email

class Countries(models.Model):
	country = models.CharField(
		max_length=100,
		choices=COUNTRY_CHOICES,
	)

	def __str__(self):
		return self.country

class CandidatePreferencesEmployerType(models.Model):
	employer_type = models.CharField(
		max_length=100,
		choices=EMPLOYER_TYPE_CHOICES,
	)
	def __str__(self):
		return self.employer_type

class CandidatePreferencesPositionType(models.Model):
	job_title = models.CharField(
		max_length=10,
		choices=POSITION_TYPE_CHOICES
	)
	def __str__(self):
		return self.job_title				

class CandidatePreferences(models.Model):
	candidate = models.OneToOneField(
		Candidate,
		on_delete=models.CASCADE,
	)
	location = models.ManyToManyField(Countries, blank=True)
	employer_type = models.ManyToManyField(CandidatePreferencesEmployerType, blank=True)
	desired_job_title = models.ManyToManyField(CandidatePreferencesPositionType, blank=True)
	desired_monthlty_salary = models.CharField(
		blank=True,
		max_length=10,
		choices=DESIRED_MONTHLY_SALARY_CHOICES
	)

	def __str__(self):
		return self.candidate.email

class Recruiter(BaseUser):
	phone_number = PhoneNumberField()
	date_of_birth = models.DateField(blank=True)
	location = models.CharField(blank=True, max_length=100)
	id_card = models.ImageField(upload_to='%Y/%m/%d')
	# candidate = models.OneToOneField(
	# 	Employer,
	# 	on_delete=models.CASCADE,
	# )
	USERNAME_FIELD = 'pk'

	def __str__(self):
		return self.email