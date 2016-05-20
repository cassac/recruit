from django.shortcuts import render
from .models import Recruiter

def view_recruiters(request):
	recruiters = Recruiter.objects.all()
	context = {'recruiters': recruiters}
	return render(request, 'recruiters/recruiters.html', context)