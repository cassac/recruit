# Choices used for M2M tables are actually not used in
# varChar fields. They must be manually inserted into db.

import pytz
from django_countries import countries

TIMEZONE_CHOICES = tuple((choice, choice) for choice in pytz.common_timezones)

COUNTRY_CHOICES = tuple(countries)

GENDER_CHOICES = (
				('',''),
				('male','Male'),
				('female', 'Female'),
			)

EDUCATION_CHOICES = (
				('',''),
				('High School','High School'),
				('Vocational School', 'Vocational School'),
				('Community College','Community College'),
				("Bachelor's Degree", "Bachelor's Degree"),
				("Master's Degree", "Master's Degree"),
				('MBA', 'MBA'),
				('PhD', 'PhD'),						
			)

EMPLOYER_TYPE_CHOICES = (
			('University', 'University'), 
			('High School', 'High School'),
			('Middle School', 'Middle School'), 
			('Primary School', 'Primary School'),
			('Kindergarten', 'Kindergarten'),
			('Youth Language Center', 'Youth Language Center'),
			('Adult Language Center', 'Adult Language Center'),			
		)

POSITION_TYPE_CHOICES = (
			('Teacher', 'Teacher'),
			('Manager', 'Manager'),
			('Principal', 'Principal'),
			('Partner', 'Partner'), 									
		)

DESIRED_MONTHLY_SALARY_CHOICES = (
			('1000', '1000+'), 
			('2000', '2000+'), 
			('3000', '3000+'),
			('4000', '4000+'), 
			('5000', '5000+'),
			('6000', '6000+'), 
			('7000', '7000+'),
			('8000', '8000+'), 
			('9000', '9000+'),
			('10000', '10000+'),
			('11000', '11000+'), 
			('12000', '12000+'),
			('13000', '13000+'),
			('14000', '14000+'),
			('15000', '15000+'), 
			('16000', '16000+'),
			('17000', '17000+'),
			('18000', '18000+'),
			('19000', '19000+'),
			('20000', '20000+'),
			('21000', '21000+'),
			('22000', '22000+'),
			('23000', '23000+'),
			('24000', '24000+'),
			('25000', '25000+'),								 
		)