from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (BaseUser, Candidate, CandidatePreferences, Recruiter, 
	Company, CompanyPreferences)

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password',
		widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation',
		widget=forms.PasswordInput)

	class Meta:
		model = BaseUser
		fields = ('email',)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('Passwords don\'t match')

		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = BaseUser
		fields = ('email', 'password', 'is_active', 'is_admin')

	def clean_password(self):
		return self.initial['password']

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email','is_admin')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Permissions', {'fields': ('is_admin',)}),
	)
	add_fieldsets = (
		(None, {
		'classes': ('wide',),
		'fields': ('email', 'password1', 'password2')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(BaseUser, UserAdmin)
admin.site.unregister(Group)

class CandidatePreferencesInline(admin.StackedInline):
	model = CandidatePreferences
	can_delete = False
	verbose_name_plural = 'Preferences'

class CandidateAdmin(admin.ModelAdmin):
	inlines = (CandidatePreferencesInline,)
	exclude = ('password', 'last_login', 'is_admin',)

admin.site.register(Candidate, CandidateAdmin)


class RecruiterAdmin(admin.ModelAdmin):
	exclude = ('password', 'last_login', 'is_admin',)

admin.site.register(Recruiter, RecruiterAdmin)

class CompanyAdmin(admin.ModelAdmin):
	exclude = ('password', 'last_login', 'is_admin',)

admin.site.register(Company, CompanyAdmin)

class CompanyPreferencesAdmin(admin.ModelAdmin):
	pass

admin.site.register(CompanyPreferences, CompanyPreferencesAdmin)