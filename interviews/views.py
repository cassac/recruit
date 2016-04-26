import json
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

from interviews.models import Available
from accounts.models import BaseUser

def available(request, bu_id):
	user = BaseUser.objects.get(id=bu_id)

	if request.method == 'GET':
		context = {'user': user.first_name, 'timezone': ''}

	if request.method == 'POST':
		old_availability = user.available_set.all()
		new_availability = json.loads(request.POST.get('availability'))
		available_instances = []
		for day, times in new_availability.items():
			for time in times:
				avail = Available(
							day_of_week=int(day), 
							time_start=time['start'], 
							time_end=time['end'],
							baseuser=user
						)
				available_instances.append(avail)
		old_availability.delete()
		Available.objects.bulk_create(available_instances)
		context = {'message': 'success'}
		return JsonResponse({'message':'Availability Updated'})

	return render(request, 'interviews/available.html', context)