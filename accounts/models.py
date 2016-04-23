from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from .choices import (TIMEZONE_CHOICES, COUNTRY_CHOICES, GENDER_CHOICES,
	EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES, POSITION_TYPE_CHOICES, 
	DESIRED_MONTHLY_SALARY_CHOICES)

def load_m2m_choices():

	for choice in COUNTRY_CHOICES:
		Country(
			country=choice[1]
		).save()

	for choice in GENDER_CHOICES:
		Gender(
			gender=choice[1]
		).save()

	for choice in EMPLOYER_TYPE_CHOICES:

		CandidatePreferencesEmployerType(
				employer_type=choice[1]
			).save()

	for choice in POSITION_TYPE_CHOICES:

		CandidatePreferencesPositionType(
				job_title=choice[1]
			).save()

class BaseUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email,
			password=password
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class BaseUser(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True, verbose_name='email address')
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

	objects = BaseUserManager()

	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

class Candidate(BaseUser):
	date_of_birth = models.DateField(blank=True, null=True)
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

class Country(models.Model):
	country = models.CharField(
		max_length=100,
		choices=COUNTRY_CHOICES,
	)

	def __str__(self):
		return self.country

class Gender(models.Model):
	gender = models.CharField(
		max_length=100,
		choices=GENDER_CHOICES,
	)

	def __str__(self):
		return self.gender

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
	location = models.ManyToManyField(Country, blank=True)
	employer_type = models.ManyToManyField(CandidatePreferencesEmployerType, blank=True)
	desired_job_title = models.ManyToManyField(CandidatePreferencesPositionType, blank=True)
	desired_monthlty_salary = models.CharField(
		blank=True,
		max_length=10,
		choices=DESIRED_MONTHLY_SALARY_CHOICES
	)

	def __str__(self):
		return self.candidate.email

class Company(BaseUser):
	phone_number = PhoneNumberField(blank=False)
	name_english = models.CharField(blank=False, max_length=200)
	name_local = models.CharField(blank=False, max_length=200)
	address_english = models.CharField(blank=False, max_length=200)
	address_local = models.CharField(blank=False, max_length=200)
	business_license = models.ImageField(upload_to='%Y/%m/%d')

	def __str__(self):
		return self.name_english

class CompanyPreferences(models.Model):
	company = models.OneToOneField(
		Company,
		on_delete=models.CASCADE,
	)
	education = models.CharField(
			max_length=25,
			blank=True,
			choices=EDUCATION_CHOICES,
		)
	education_major = models.CharField(max_length=50, blank=True)
	age_range_low = models.IntegerField(blank=True)
	age_range_high = models.IntegerField(blank=True)
	years_of_experience = models.IntegerField(blank=True)
	citizenship = models.ManyToManyField(Country, blank=True)

	def __str__(self):
		return self.company.name_english

class Recruiter(BaseUser):
	phone_number = PhoneNumberField(blank=False)
	date_of_birth = models.DateField(blank=True, null=True)
	location = models.CharField(blank=True, max_length=100)
	id_card = models.ImageField(upload_to='%Y/%m/%d')
	companies = models.ManyToManyField(Company, blank=False)
	USERNAME_FIELD = 'pk'

	def __str__(self):
		return self.email
