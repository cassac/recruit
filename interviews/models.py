import shortuuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from candidates.models import Candidate
from jobs.models import Job

STATUS_CHOICES = (
	(-3, 'Revoked'),
	(-2, 'Candidate Cancelled'),
	(-1, 'Employer Cancelled'),
	(0, 'Request Open'),
	(1, 'Pending Confirmation'),
	(2, 'Confirmed'),
	(3, 'Completed'),
)

class InterviewInvitation(models.Model):
	uuid = models.CharField(primary_key=True, 
		max_length=5,
		default=shortuuid.ShortUUID().random(length=5).upper(),
		)
	candidate = models.ForeignKey(Candidate)
	job = models.ForeignKey(Job)
	confirmed_time = models.DateTimeField(null=True, blank=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	request_reminders_sent = models.IntegerField(default=0)
	confirmation_reminders_sent = models.IntegerField(default=0)
	is_active = models.BooleanField(default=1)
	result = models.CharField(max_length=50, blank=True)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return '<Interview C: %s B: %s>' % (self.candidate.user.email, self.job.title)

class InterviewRequest(models.Model):
	candidate = models.ForeignKey(Candidate)
	job = models.ForeignKey(Job)
	candidate_accepted = models.NullBooleanField()
	employer_accepted = models.NullBooleanField()
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

def generate_invitation(sender, instance, created, **kwargs):
	if instance.candidate_accepted and instance.employer_accepted:
		InterviewInvitation.objects.create(
			candidate=instance.candidate,
			job=instance.job
		)

post_save.connect(generate_invitation, sender=InterviewRequest)	

class Available(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)	
	day_of_week = models.IntegerField()
	time_start = models.CharField(max_length=5)
	time_end = models.CharField(max_length=5)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)	

	def __str__(self):
		return 'day(%s) %s-%s' % (self.day_of_week, self.time_start, self.time_end)


class Exclusion(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)	
	date = models.DateField()
