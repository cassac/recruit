from django.contrib import admin

from .models import Employer, EmployerRequirements

class EmployerRequirementsInline(admin.StackedInline):
	model = Employer
	can_delete = False
	verbose_name_plural = 'Preferences'

class EmployerAdmin(admin.ModelAdmin):
	# inlines = (EmployerRequirementsInline,)
	exclude = ('password', 'last_login', 'is_staff', 'business_license_thumb')

admin.site.register(Employer, EmployerAdmin)