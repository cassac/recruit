from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile
from .forms import UserApplyStep1Form, UserApplyStep2Form

def apply_step_1(request):

	key = request.GET.get('key', None)

	if not key and request.method == 'POST':
		
		form = UserApplyStep1Form(request.POST)

		if form.is_valid:
			data = form.data
			first_name = data['first_name']
			last_name = data['last_name']
			email = data['email']
			citizenship = data['citizenship']
			skype_id = data['skype_id']
			timezone = data['timezone']

			user, created = User.objects.get_or_create(
				first_name=first_name,
				last_name=last_name,
				email=email,
				username=email
				)

			if not created:
				messages.add_message(request, messages.ERROR,
					email + ' has already been registered.')
			else:
				userprofile = UserProfile(
					user=user,
					timezone=timezone,
					citizenship=citizenship,
					skype_id=skype_id,
					user_type='Candidate'
					)
				userprofile.save()

	elif not key and request.method == 'GET':
		form = UserApplyStep1Form()

	elif key and request.method == 'GET':
		form = UserApplyStep2Form()

	elif key and request.method == 'POST':
		form = UserApplyStep2Form(request.POST)

	return render(request, 'candidates/apply.html', {'form': form})