from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.core import signing
from django.core.signing import SignatureExpired, BadSignature

from jobs.models import Job
from recruit.choices import (EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES)

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
	image = models.ImageField(upload_to='employer/%Y/%m/%d')
	thumb = models.ImageField(upload_to='employer/%Y/%m/%d', blank=True)
	is_active = models.BooleanField(default=True)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

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
		return user.candidate

def update_user_profile(sender, instance, created, **kwargs):
	from accounts.models import UserProfile
	if created:
		UserProfile.objects.filter(user=instance.user).update(user_type='Candidate')

post_save.connect(update_user_profile, sender=Candidate)		

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