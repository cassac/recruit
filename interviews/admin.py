from django.contrib import admin

from .models import InterviewRequest, InterviewInvitation, Available

class InterviewRequestAdmin(admin.ModelAdmin):
	list_display = ('candidate', 'candidate_accepted', 'job', 'employer_accepted')	
	search_fields = ('candidate__user__username', 'candidate__user__email',
		'candidate__user__first_name', 'candidate__user__last_name',
		'job__employer__user__username', 'job__employer__user__email',
		'job__employer__user__first_name', 'job__employer__user__last_name',
		'job__employer__name_english', 'job__employer__name_local',)

admin.site.register(InterviewRequest, InterviewRequestAdmin)

class InterviewInvitationAdmin(admin.ModelAdmin):

	search_fields = ('uuid', 'candidate__user__username', 'candidate__user__email',
		'candidate__user__first_name', 'candidate__user__last_name',
		'job__employer__user__username', 'job__employer__user__email',
		'job__employer__user__first_name', 'job__employer__user__last_name',
		'job__employer__name_english', 'job__employer__name_local',)
	list_display = ('candidate', 'job', 'status', 'confirmed_time', 'uuid')	
	list_filter = ('status', 'confirmed_time',)

admin.site.register(InterviewInvitation , InterviewInvitationAdmin)

class AvailableAdmin(admin.ModelAdmin):
	pass

admin.site.register(Available, AvailableAdmin)
