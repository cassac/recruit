from django.contrib import admin

from .models import InterviewRequest

class InterviewRequestAdmin(admin.ModelAdmin):
	pass

admin.site.register(InterviewRequest, InterviewRequestAdmin)