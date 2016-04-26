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
		availability_dict = {}
		for avail in user_availabiity:
			temp = {"start": avail.time_start, "end": avail.time_end}
			day_of_week = str(avail.day_of_week)
			if day_of_week not in availability_dict:
				availability_dict[day_of_week] = []
			availability_dict[day_of_week].append(temp)
		availability = json.dumps(availability_dict)
		print(availability)
		return JsonResponse({'availability': availability})

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
