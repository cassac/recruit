from django.contrib import admin

from .models import CandidateRequirements, CandidateDocument, Candidate, RequestedJob

class RequestedJobInline(admin.StackedInline):
	model = RequestedJob

class CandidateRequirementsInline(admin.StackedInline):
	model = CandidateRequirements

class CandidateDocument(admin.StackedInline):
	model = CandidateDocument

class CandidateAdmin(admin.ModelAdmin):
	# inlines = (CandidateRequirementsInline,)
	inlines = (CandidateDocument, RequestedJobInline)
	exclude = ('password', 'last_login', 'is_admin', 'thumb')

admin.site.register(Candidate, CandidateAdmin)

