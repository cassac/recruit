from django.shortcuts import render
from django.contrib import messages

def available(request):
	messages.add_message(request, messages.SUCCESS, 'Message here')
	context = {'foo': 'bar'}
	return render(request, 'interviews/available.html', context)