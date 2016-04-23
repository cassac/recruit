from django.db import models

from accounts.models import Company, Recruiter, Gender, Country

class Job(models.Model):
	company = models.OneToOneField(
		Company,
		on_delete=models.CASCADE,
	)
	title = models.CharField(max_length=100)
	weekly_hours = models.IntegerField()
	salary_high = models.IntegerField()
	salary_low = models.IntegerField()
	accommodation_included = models.BooleanField()
	accommodation_stipend = models.CharField(max_length=100)
	travel_stipend = models.CharField(max_length=100)
	insurance_included = models.BooleanField()
	insurance_stipend = models.CharField(max_length=100)
	contract_length = models.IntegerField()
	contract_renew_bonus = models.IntegerField(blank=True)
	contract_completion_bonus = models.IntegerField(blank=True)
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
	is_featured = models.NullBooleanField()
	is_promoting = models.NullBooleanField()
	recruiter = models.ManyToManyField(Recruiter, blank=True)

	def __str__(self):
		return self.title

class JobPreferences(models.Model):
	job = models.OneToOneField(
		Job,
		on_delete=models.CASCADE,
	)
	age_high = models.IntegerField()
	age_low = models.IntegerField()
	gender = models.ManyToManyField(Gender, blank=True) 	
	citizenship = models.ManyToManyField(Country, blank=True)		