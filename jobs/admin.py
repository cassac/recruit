from django.contrib import admin

from .models import Job, JobPreferences

class JobPreferencesInline(admin.StackedInline):
	model = JobPreferences
	can_delete = False
	verbose_name_plural = 'Preferences'

class JobAdmin(admin.ModelAdmin):
	inlines = (JobPreferencesInline,)

admin.site.register(Job, JobAdmin)