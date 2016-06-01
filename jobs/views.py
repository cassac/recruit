from django.http import HttpResponseRedirect
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
			reverse_url = reverse('account_login')
			jobs_ids_string = ','.join(jobs_ids)
			query_string = '?jobs={}'.format(jobs_ids_string)
			return HttpResponseRedirect(reverse_url + query_string)

		context = {}
		
	return render(request, 'jobs/jobs.html', context)

def view_job_details(request, job_id):
	job = Job.objects.get(id=job_id)
	context = {'job': job}
	return render(request, 'jobs/details.html', context)