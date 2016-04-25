import shortuuid
from django.db import models
from accounts.models import BaseUser

STATUS_CHOICES = (
	(-3, 'Revoked'),
	(-2, 'Party A Cancelled'),
	(-1, 'Party B Cancelled'),
	(0, 'Request Open'),
	(1, 'Pending Confirmation'),
	(2, 'Confirmed'),
	(3, 'Completed'),
)

class InterviewRequest(models.Model):
	uuid = models.CharField(primary_key=True, 
		max_length=5,
		default=shortuuid.ShortUUID().random(length=5).upper(),
		)
	party_a = models.OneToOneField(BaseUser, related_name='party_a') 
	party_b = models.OneToOneField(BaseUser, related_name='party_b')
	confirmed_time = models.DateTimeField(null=True, blank=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	request_reminders_sent = models.IntegerField(default=0)
	is_active = models.BooleanField(default=1)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return '<Interview: A: %s, B: %s>' % (self.party_a, self.party_b)

class Available(models.Model):
	day_of_week = models.IntegerField()
	timeslot_begin = models.CharField(max_length=5)
	timeslot_end = models.CharField(max_length=5)
	baseuser = models.OneToOneField(BaseUser)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)	

	def __str__(self):
		return '<Available: day(%s) %s-%s>' % (self.day_of_week, self.timeslot_begin, self.timeslot_end)


class Exclusion(models.Model):
	date = models.DateField()
	baseuser = models.OneToOneField(BaseUser)
