from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from interviews.models import InterviewInvitation, InterviewRequest
from jobs.models import Job

@login_required
def dashboards(request):
	if request.user.is_authenticated:

		user_type = request.user.userprofile.user_type

		if user_type == 'Candidate':
			return render(request, 'candidates/dashboard.html')

		if user_type == 'Recruiter':

			interviews_pending_confirmation =\
				InterviewInvitation.objects.exclude(
					confirmed_time__isnull=False,
				).count()

			interviews_pending_follow_up =\
				InterviewInvitation.objects.exclude(
					confirmed_time__isnull=True,
					result='',
				).count()

			pending_employer_requests =\
				InterviewRequest.objects.filter(
					employer_accepted=True,
					candidate_accepted__isnull=True,
				).count()

			pending_candidate_requests =\
				InterviewRequest.objects.filter(
					candidate_accepted=True,
					employer_accepted__isnull=True,
				).count()
				
			context = {
				'interviews_pending_confirmation': interviews_pending_confirmation,
				'interviews_pending_follow_up': interviews_pending_follow_up,
				'pending_employer_requests': pending_employer_requests,
				'pending_candidate_requests': pending_candidate_requests,
			}

			return render(request, 'recruiters/dashboard.html',
				context)

		if user_type == 'Employer':
			return render(request, 'employers/dashboard.html')	

	return render(request, 'home.html')	