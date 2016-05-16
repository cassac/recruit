from django.db import models

from recruiters.models import Recruiter
from employers.models import Employer
from recruit.choices import COUNTRY_CHOICES


class Country(models.Model):
	country = models.CharField(
		max_length=100,
		choices=COUNTRY_CHOICES,
	)

	def __str__(self):
		return self.country

class Job(models.Model):
	employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	location = models.CharField(choices=(('onsite', 'On-site'), ('remote', 'Remote'),), max_length=50, blank=True, null=True)
	weekly_hours = models.IntegerField()
	salary_high = models.IntegerField()
	salary_low = models.IntegerField()
	accommodation_included = models.BooleanField()
	accommodation_stipend = models.CharField(max_length=100)
	travel_stipend = models.CharField(max_length=100)
	insurance_included = models.BooleanField()
	insurance_stipend = models.CharField(max_length=100)
	contract_length = models.IntegerField()
	contract_renew_bonus = models.IntegerField(blank=True, null=True)
	contract_completion_bonus = models.IntegerField(blank=True, null=True)
	compensation_type = models.CharField(
		max_length=25, 
		blank=False,
		choices=(
			('One-time', 'One-time'),		 
			('Monthly', 'Monthly'),
		)
	)	
	compensation_amount = models.CharField(max_length=25, blank=False)
	compensation_terms = models.CharField(max_length=250)
	is_featured = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	recruiter = models.ForeignKey(Recruiter)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return "%d) %s: %s" % (self.pk, self.employer.name_english, self.title)

class JobRequirements(models.Model):
	job = models.OneToOneField(Job, on_delete=models.CASCADE)
	age_high = models.IntegerField()
	age_low = models.IntegerField()
	gender = models.CharField(choices=(('male', 'Male'), ('female', 'Female'),), max_length=10, blank=True, null=True)
	citizenship = models.ManyToManyField(Country, blank=True)		