from django.shortcuts import render
from .models import Job

def view_jobs(request):
	jobs = Job.objects.all()
	context = {'jobs': jobs}
	return render(request, 'jobs/jobs.html', context)

def view_job_details(request, job_id):
	job = Job.objects.get(id=job_id)
	context = {'job': job}
	return render(request, 'jobs/details.html', context)