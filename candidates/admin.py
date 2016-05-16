from django.contrib import admin

from .models import CandidateRequirements, CandidateDocument, Candidate

class CandidateRequirementsInline(admin.StackedInline):
	model = CandidateRequirements
	can_delete = False

class CandidateDocument(admin.StackedInline):
	model = CandidateDocument
	can_delete = True

class CandidateAdmin(admin.ModelAdmin):
	# inlines = (CandidateRequirementsInline,)
	inlines = (CandidateDocument,)
	exclude = ('password', 'last_login', 'is_admin', 'thumb')

admin.site.register(Candidate, CandidateAdmin)

