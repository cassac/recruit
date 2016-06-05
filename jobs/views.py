from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .models import Job

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
		messages.add_message(request, messages.SUCCESS,
			'Form submitted successfully.')
	return render(request, 'jobs/jobs.html', context)

def view_job_details(request, job_id):
	job = Job.objects.get(id=job_id)
	context = {'job': job}
	return render(request, 'jobs/details.html', context)