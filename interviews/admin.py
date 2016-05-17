from django.contrib import admin

from .models import InterviewRequest, InterviewInvitation, Available

class InterviewRequestAdmin(admin.ModelAdmin):
	pass

admin.site.register(InterviewRequest, InterviewRequestAdmin)

class InterviewInvitationAdmin(admin.ModelAdmin):
	readonly_fields = ('uuid',)
	search_fields = ('uuid',)
	list_display = ('status', 'confirmed_time', 'uuid')	
	list_filter = ('status', 'confirmed_time',)

admin.site.register(InterviewInvitation , InterviewInvitationAdmin)

class AvailableAdmin(admin.ModelAdmin):
	pass

admin.site.register(Available, AvailableAdmin)
