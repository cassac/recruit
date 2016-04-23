import datetime

from django.test import TestCase, Client
from .models import BaseUser, Candidate

def get_baseuser(id):
	return BaseUser.objects.get(id=id)

def get_candidate(id):
	return Candidate.objects.get(id=id)

class BaseUserTestCase(TestCase):
	def setUp(self):
		baseuser = BaseUser.objects.create(
				email='email@example.com',
				first_name='John',
				last_name='Doe',
			)
		baseuser.set_password('password')
		baseuser.is_admin=True
		baseuser.save()

	def test_baseuser_creation(self):
		baseuser = get_baseuser(1)
		self.assertEqual(baseuser.email, 'email@example.com')
		self.assertEqual(baseuser.first_name, 'John')

	def test_baseuser_password(self):
		baseuser = get_baseuser(1)
		self.assertTrue(baseuser.check_password('password'))

class CandidateTestCase(TestCase):
	def setUp(self):
		self.client = Client()

		candidate = Candidate.objects.create(
				email='email@example.com',
				first_name='John',
				last_name='Doe',
				citizenship='Antarctica',
				timezone='Antarctica',
				date_of_birth=datetime.date(1970, 1, 1),
				available=datetime.datetime.today()
			)
		candidate.set_password('password')
		candidate.save()

	def test_candidate_creation(self):
		candidate = Candidate.objects.get(first_name='John')
		self.assertEqual(candidate.email, 'email@example.com')
		self.assertEqual(candidate.first_name, 'John')

	def test_candidate_unauthorized_login(self):
		candidate = get_candidate(1)
		response = self.client.post('/admin/login/', {'email': candidate.email, 
												'password': 'password'})
		self.assertTrue(response.status_code==200)
