import json
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

from interviews.models import Available
from accounts.models import BaseUser

# {'3': [{'end': '05:30', 'start': '00:00'}, {'end': '21:30', 'start': '15:00'}], 
# '1': [{'end': '18:00', 'start': '17:00'}], '0': [{'end': '21:00', 'start': '15:00'}],
#  '2': [{'end': '23:59', 'start': '23:00'}]}

# ad:  {'2': [{'start': '23:00', 'end': '23:59'}], '3': [{'start': '00:00', 'end': '05:30'}, {'start': '15:00', 'end': '21:30'}], '1': [{'start': '17:00', 'end': '18:00'}], '0': [{'start': '15:00', 'end': '21:00'}]}

def available(request, bu_id):
	user = BaseUser.objects.get(id=bu_id)
	context = {'user': user}

	return render(request, 'interviews/available.html', context)

def availability(request, bu_id):
	user = BaseUser.objects.get(id=bu_id)
	if request.method == 'GET':
		user_availabiity = user.available_set.all()
		availability = []
		for avail in user_availabiity:
			temp = {
				"day": str(avail.day_of_week),
				"start": avail.time_start, 
				"end": avail.time_end
			}
			availability.append(temp)

		availability = json.dumps(availability)
		print(availability)
		return JsonResponse({'availability': availability})

	if request.method == 'POST':
		old_availability = user.available_set.all()
		new_availability = json.loads(request.POST.get('availability'))
		print(new_availability)
		available_instances = []
		for time_range in new_availability:
			avail = Available(
						day_of_week=int(time_range['day']), 
						time_start=time_range['start'], 
						time_end=time_range['end'],
						baseuser=user
					)
			available_instances.append(avail)
		print(available_instances)
		old_availability.delete()
		Available.objects.bulk_create(available_instances)
		context = {'message': 'success'}
		return JsonResponse({'message':'Availability Updated'})
