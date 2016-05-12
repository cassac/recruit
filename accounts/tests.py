import datetime

import tempfile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Candidate, Employer

def get_user(id):
	return User.objects.get(id=id)

def get_candidate(id):
	return Candidate.objects.get(id=id)

class UserTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(
				email='email@example.com',
				first_name='John',
				last_name='Doe',
			)
		user.set_password('password')
		user.is_admin=True
		user.save()

	def test_user_creation(self):
		user = get_user(1)
		self.assertEqual(user.email, 'email@example.com')
		self.assertEqual(user.first_name, 'John')

	def test_user_password(self):
		user = get_user(1)
		self.assertTrue(user.check_password('password'))

	def test_candidate_creation(self):
		user = get_user(1)
		candidate = Candidate.objects.create(
				user=user,
				birth_year='1970',
				gender='male',
				education="Master's",
				education_major='Marketing',
				current_location='Antarctica',
				date_of_birth=datetime.date(1970, 1, 1),
			)
		candidate.save()
		self.assertTrue(user.candidate.user_id, 1)
		self.assertEqual(candidate.user.email, 'email@example.com')
		self.assertEqual(candidate.user.first_name, 'John')

	def test_candidate_unauthorized_login(self):
		user = get_user(1)
		response = self.client.post('/admin/login/', {'username': user.email, 
												'password': 'password'})
		self.assertTrue(response.status_code==200)

	def test_employer_creation(self):
		user = get_user(1)
		employer = Employer(
			user=user,
			phone_number='+44 20 34545454',
			name_english='Acme Corp',
			name_local='Non-english name',
			address_english='123 Long Street',
			address_local='Non-english address',
			business_license=tempfile.NamedTemporaryFile(suffix=".jpg").name
		)
		employer.save()
		self.assertEqual(employer, user.employer)