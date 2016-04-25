from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

from accounts.models import BaseUser

def available(request, bu_id):
	user = BaseUser.objects.get(id=bu_id)

	if request.method == 'GET':
		context = {'user': user.first_name, 'timezone': ''}

	if request.method == 'POST':
		context = {'message': 'success'}
		return JsonResponse({'message':'Availability Updated'})

	return render(request, 'interviews/available.html', context)