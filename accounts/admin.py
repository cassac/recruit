from django.contrib import admin
from .models import Candidate

class CandidateAdmin(admin.ModelAdmin):
	pass
admin.site.register(Candidate, CandidateAdmin)