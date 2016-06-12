from django import forms
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries
from recruit.choices import (TIMEZONE_CHOICES, EDUCATION_CHOICES,
	 GENDER_CHOICES)

class UserApplyStep1Form(forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	email = forms.EmailField(max_length=50)
	citizenship = LazyTypedChoiceField(choices=countries)
	skype_id = forms.CharField(label='Skype ID', max_length=20)
	timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES)

class UserApplyStep2Form(forms.Form):
	birth_year = forms.IntegerField(min_value=1950, max_value=2000)
	gender = forms.TypedChoiceField(choices=GENDER_CHOICES)
	education = forms.TypedChoiceField(choices=EDUCATION_CHOICES)
	education_major = forms.CharField(max_length=50)
	image = forms.ImageField()
	resume = forms.FileField()