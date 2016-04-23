import datetime

from django.test import TestCase
from .models import BaseUser, Candidate

def get_base_user():
	return BaseUser.objects.get(first_name='John')

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
		baseuser = get_base_user()
		self.assertEqual(baseuser.email, 'email@example.com')
		self.assertEqual(baseuser.first_name, 'John')

	def test_baseuser_password(self):
		baseuser = get_base_user()
		self.assertTrue(baseuser.check_password('password'))

class CandidateTestCase(TestCase):
	def setUp(self):
		Candidate.objects.create(
				email='email@example.com',
				first_name='John',
				last_name='Doe',
				citizenship='Antarctica',
				timezone='Antarctica',
				date_of_birth=datetime.date(1970, 1, 1),
				available=datetime.datetime.today()
			)

	def test_candidate_creation(self):
		candidate = Candidate.objects.get(first_name='John')
		self.assertEqual(candidate.email, 'email@example.com')
		self.assertEqual(candidate.first_name, 'John')