from django.contrib import admin

from .models import CandidateRequirements, CandidateDocument, Candidate
from interviews.models import InterviewRequest

class InterviewRequestInline(admin.StackedInline):
	model = InterviewRequest

class CandidateRequirementsInline(admin.StackedInline):
	model = CandidateRequirements

class CandidateDocument(admin.StackedInline):
	model = CandidateDocument

class CandidateAdmin(admin.ModelAdmin):
	# inlines = (CandidateRequirementsInline,)
	inlines = (CandidateDocument, InterviewRequestInline)
	exclude = ('password', 'last_login', 'is_admin', 'thumb')

admin.site.register(Candidate, CandidateAdmin)

