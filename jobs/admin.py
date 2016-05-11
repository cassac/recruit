from django.contrib import admin

from .models import Job, JobRequirements

class JobRequirementsInline(admin.StackedInline):
	model = JobRequirements
	can_delete = False
	verbose_name_plural = 'Preferences'

class JobAdmin(admin.ModelAdmin):
	inlines = (JobRequirementsInline,)

admin.site.register(Job, JobAdmin)