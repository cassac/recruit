from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

	def get_login_redirect_url(self, request):
		if 'redirect_to' in request.session:
			path = request.session['redirect_to']
			if 'add_new_jobs_pending' in request.session and\
			request.session['add_new_jobs_pending']:
				messages.add_message(request, messages.WARNING,
				'Thanks for logining in. Please submit the form.')
				del request.session['add_new_jobs_pending']
			del request.session['redirect_to']
		else:
			path = '/'
		return path