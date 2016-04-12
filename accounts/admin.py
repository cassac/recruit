from django.contrib import admin
from .models import Candidate

class CandidateAdmin(admin.ModelAdmin):
	exclude = ('password', 'last_login', 'is_admin',)

admin.site.register(Candidate, CandidateAdmin)