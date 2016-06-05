#!/usr/bin/python3
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Job
from candidates.models import Candidate
from interviews.models import InterviewRequest

def add_interview_requests(request, jobs_ids):

	try:
		candidate = request.user.candidate
	except Candidate.DoesNotExist:
		messages.add_message(request, messages.ERROR,
			'This user is not a candidate.')
		return
	except:
		raise

	for job_id in jobs_ids:
		ir = InterviewRequest(candidate=candidate, 
			job=Job.objects.get(pk=int(job_id)))
		ir.save()

	if 'requested_jobs' in request.session:
		del request.session['requested_jobs']

	messages.add_message(request, messages.SUCCESS,
		'Form submitted successfully.')

def view_jobs(request):

	if request.method == 'GET':
		jobs = Job.objects.all()
		context = {'jobs': jobs}

	if request.method == 'POST':
		jobs_ids = request.POST.getlist('requested_jobs[]')

		if request.user.is_anonymous():
			request.session['add_new_jobs_pending'] = True
			request.session['requested_jobs'] = jobs_ids
			request.session['redirect_to'] = reverse('jobs')
			return HttpResponseRedirect(reverse('account_login'))

		context = {}

		add_interview_requests(request, jobs_ids)

	return render(request, 'jobs/jobs.html', context)

def view_job_details(request, job_id):
	job = Job.objects.get(id=job_id)
	context = {'job': job}
	return render(request, 'jobs/details.html', context)