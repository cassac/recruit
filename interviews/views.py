from django.shortcuts import render
from django.contrib import messages

from accounts.models import BaseUser

def available(request, bu_id):
	user = BaseUser.objects.get(id=bu_id)
	messages.add_message(request, messages.SUCCESS, 'Message here')
	context = {'user': user.first_name}
	return render(request, 'interviews/available.html', context)