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
	party_a = models.ManyToManyField(BaseUser, related_name='party_a') 
	party_b = models.ManyToManyField(BaseUser, related_name='party_b')
	confirmed_time = models.DateTimeField(null=True, blank=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	is_active = models.BooleanField(default=1)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
