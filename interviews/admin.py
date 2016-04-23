from django.contrib import admin

from .models import InterviewRequest

class InterviewRequestAdmin(admin.ModelAdmin):
	search_fields = ('party_a', 'party_b')
	list_display = ('party_a', 'party_b', 'status', 'confirmed_time')	
	list_filter = ('status', 'confirmed_time',)

admin.site.register(InterviewRequest, InterviewRequestAdmin)