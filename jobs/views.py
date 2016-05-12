from django.shortcuts import render
from .models import Job

def view_jobs(request):
	jobs = Job.objects.all()
	context = {'jobs': jobs}
	return render(request, 'jobs/jobs.html', context)