from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import (Candidate, CandidateRequirements, Recruiter, Employer, 
	EmployerRequirements)

class UserCreationForm(forms.ModelForm):


	class Meta:
		model = User
		fields = ('email', 'username')

	def clean(self):
		super(UserCreationForm, self).clean()
		cleaned_data = self.cleaned_data
		if User.objects.filter(email=cleaned_data['email']).exists():
			raise ValidationError('Email already registered')
		return cleaned_data

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.username = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'is_active', 'is_staff')

	def clean_password(self):
		return self.initial['password']

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email','is_staff')
	list_filter = ('is_staff',)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'username')}),
		('Permissions', {'fields': ('is_staff',)}),
	)
	add_fieldsets = (
		(None, {
		'classes': ('wide',),
		'fields': ('email','username')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CandidateRequirementsInline(admin.StackedInline):
	model = CandidateRequirements
	can_delete = False


class CandidateAdmin(admin.ModelAdmin):
	# inlines = (CandidateRequirementsInline,)
	exclude = ('password', 'last_login', 'is_admin',)

admin.site.register(Candidate, CandidateAdmin)


class RecruiterAdmin(admin.ModelAdmin):
	exclude = ('password', 'last_login', 'is_staff',)

admin.site.register(Recruiter, RecruiterAdmin)

class EmployerRequirementsInline(admin.StackedInline):
	model = Employer
	can_delete = False
	verbose_name_plural = 'Preferences'

class EmployerAdmin(admin.ModelAdmin):
	# inlines = (EmployerRequirementsInline,)
	exclude = ('password', 'last_login', 'is_staff',)

admin.site.register(Employer, EmployerAdmin)