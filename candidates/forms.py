from django import forms
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries
from recruit.choices import TIMEZONE_CHOICES

class UserApplyForm(forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	email = forms.EmailField()
	citizenship = LazyTypedChoiceField(choices=countries)
	skype_id = forms.CharField(max_length=20)
	timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES)