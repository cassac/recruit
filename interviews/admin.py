from django.contrib import admin

from .models import InterviewRequest

class InterviewRequestAdmin(admin.ModelAdmin):
	readonly_fields = ('uuid',)
	search_fields = ('uuid', 'party_a', 'party_b')
	list_display = ('party_a', 'party_b', 'status', 'confirmed_time', 'uuid')	
	list_filter = ('status', 'confirmed_time',)

admin.site.register(InterviewRequest, InterviewRequestAdmin)