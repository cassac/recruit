from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from jobs.models import Job

from recruit.choices import (TIMEZONE_CHOICES, COUNTRY_CHOICES, GENDER_CHOICES,
	EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES, POSITION_TYPE_CHOICES, 
	DESIRED_MONTHLY_SALARY_CHOICES)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	timezone = models.CharField(max_length=50, blank=True)
	citizenship = models.CharField(max_length=50, blank=True)
	user_type = models.CharField(
		choices = (('Candidate', 'Candidate'), ('Recruiter', 'Recruiter'), ('Employer', 'Employer'),),
		max_length = 50,
		default = False,
	)
	is_admin = models.BooleanField(default=False)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.user.email

class Candidate(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	birth_year = models.CharField(max_length=4, blank=False)
	date_of_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(choices=(('male', 'Male'), ('female', 'Female'),), max_length = 10, blank=True, null=True)
	education = models.CharField(
			max_length=25,
			blank=True,
			choices=EDUCATION_CHOICES,
		)	
	education_major = models.CharField(max_length=250, blank=True)
	current_location = CountryField(blank=True)
	applied_jobs = models.ManyToManyField(Job, blank=True)
	image = models.ImageField(upload_to='employer/%Y/%m/%d')
	thumb = models.ImageField(upload_to='employer/%Y/%m/%d', blank=True)

	def save(self, *args, **kwargs):
		from recruit.utils import generate_thumbnail
		self.thumb = generate_thumbnail(self.image)
		super(Candidate, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		from recruit.utils import delete_from_s3
		delete_from_s3([self.image, self.thumb])
		super(Candidate, self).delete(*args, **kwargs)	


	def __str__(self):
		return self.user.email

class CandidateRequirements(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# location = models.ManyToManyField(Location, on_delete=models.CASCADE)  create m2m
	employer_type = models.CharField(
			max_length=25,
			blank=True,
			choices=EMPLOYER_TYPE_CHOICES,
		)

class CandidateDocument(models.Model):
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	document = models.FileField(upload_to='candidate/%Y/%m/%d')	
	document_type = models.CharField(max_length=50)
	is_active = models.BooleanField(default=1)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def delete(self, *args, **kwargs):
		from recruit.utils import delete_from_s3
		delete_from_s3([self.document])
		super(CandidateDocument, self).delete(*args, **kwargs)	