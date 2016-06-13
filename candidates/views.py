from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from accounts.models import UserProfile

from .models import Candidate, CandidateDocument
from .forms import UserApplyStep1Form, UserApplyStep2Form

def apply(request):

	key = request.GET.get('key', None)
	user = UserProfile.verify_token(key)

	if not key and request.method == 'POST':
		
		form = UserApplyStep1Form(request.POST)

		if form.is_valid():
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
				
				key = user.userprofile.generate_token()
				
				return HttpResponseRedirect(
					reverse('candidate_apply') + '?key=' + key)


	elif not key and request.method == 'GET':
		form = UserApplyStep1Form()

	elif key and user and request.method == 'POST':

		form = UserApplyStep2Form(request.POST, request.FILES)
	
		if form.is_valid():
			files = form.files
			data = form.data
	
			try:
				candidate = user.candidate
				candidate.birth_year = data['birth_year']
				candidate.gender = data['gender']
				candidate.education = data['education']
				candidate.education_major = data['education_major']
				candidate.image = files['image']
				candidate.save()
			except Candidate.DoesNotExist:
				candidate = Candidate.objects.create(user=user, 
					birth_year=data['birth_year'],
					gender=data['gender'],
					education=data['education'],
					education_major=data['education_major'],
					image=files['image']
					)
			CandidateDocument.objects.create(
				candidate=candidate,
				document=files['resume'],
				document_type='Resume'
				)

			messages.add_message(request, messages.SUCCESS,
				'Form submitted successfully.')

			return HttpResponseRedirect(
					reverse('candidate_apply_success') + '?key=' + key)

	elif key and user and request.method == 'GET':
		form = UserApplyStep2Form()

	else:
		messages.add_message(request, messages.ERROR,
			'A valid application key is required to submit documents. ' +
			'Please contact the administrator.')
		form = None

	return render(request, 'candidates/apply.html', {'form': form})

def apply_success(request):
	key = request.GET.get('key', None)
	user = UserProfile.verify_token(key)

	if not key or not user:
		messages.add_message(request, messages.ERROR,
			'A valid application key is required to view this page.')
	else:
		jobs_url = reverse('jobs') + '?key=' + key
		availability_url = reverse('available', args=[user.id]) + '?key=' + key

	return render(request, 'candidates/apply.html', 
			{'success': 'success',
			 'jobs_url': jobs_url,
			 'availability_url': availability_url
			})