import json
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from interviews.models import Available


def available(request, bu_id):
	user = User.objects.get(id=bu_id)
	context = {'user': user}
	return render(request, 'interviews/available.html', context)

def availability(request, bu_id):
	user = User.objects.get(id=bu_id)
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
		return JsonResponse({'availability': availability})

	if request.method == 'POST':
		old_availability = user.available_set.all()
		new_availability = json.loads(request.POST.get('availability'))
		timezone = json.loads(request.POST.get('timezone'))
		available_instances = []
		for time_range in new_availability:
			avail = Available(
						day_of_week=int(time_range['day']), 
						time_start=time_range['start'], 
						time_end=time_range['end'],
						user=user
					)
			available_instances.append(avail)
		old_availability.delete()
		Available.objects.bulk_create(available_instances)
		message = {'message': 'Availability updated'}
		if timezone != user.userprofile.timezone:
			user.userprofile.timezone = timezone
			user.userprofile.save()
			message['message'] = 'Timezone and ' + message['message']	
		return JsonResponse(message)

