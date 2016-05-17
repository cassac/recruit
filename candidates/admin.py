from django.contrib import admin

from .models import CandidateRequirements, CandidateDocument, Candidate
from interviews.models import InterviewRequest
from accounts.models import UserProfile

class InterviewRequestInline(admin.StackedInline):
	model = InterviewRequest

class CandidateRequirementsInline(admin.StackedInline):
	model = CandidateRequirements

class CandidateDocument(admin.StackedInline):
	model = CandidateDocument

class CandidateAdmin(admin.ModelAdmin):

	def email(obj):
		return ('%s' % (obj.user.email))
	email.admin_order_field = 'user__email'

	def name(obj):
		return ('%s' % (obj.user.get_full_name()))

	def citizenship(obj):
		return ('%s' % (obj.user.userprofile.citizenship))
	citizenship.admin_order_field = 'user__userprofile__citizenship'

	def date_of_birth(obj):
		return ('%s' % (obj.date_of_birth or obj.birth_year))
	date_of_birth.admin_order_field = 'date_of_birth' 

	# inlines = (CandidateRequirementsInline,)
	list_filter = ('user__userprofile__citizenship', 'gender')
	list_display = (email, name, citizenship, date_of_birth, 'gender')	
	inlines = (CandidateDocument, InterviewRequestInline)
	exclude = ('password', 'last_login', 'is_admin', 'thumb')
	search_fields = ('date_of_birth', 'birth_year', 'user__email', 
		'user__first_name', 'user__last_name', 'user__userprofile__citizenship',)

admin.site.register(Candidate, CandidateAdmin)

