from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserCreationForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('email', 'username',)

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

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	max_num = 1
	can_delete = False

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	inlines = (UserProfileInline,)
	list_display = ('email','is_staff')
	list_filter = ('is_staff',)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'username',)}),
		('Permissions', {
			'fields': (
				'is_staff', 
				'groups',
				'user_permissions'
			),
			'classes': ('collapse',)
		}),
	)
	add_fieldsets = (
		(None, {
		'classes': ('wide',),
		'fields': ('email','username', 'first_name', 'last_name',)}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.unregister(User)
admin.site.register(User, UserAdmin)