import datetime

from django.test import TestCase
from .models import Candidate

class CandidateTestCase(TestCase):
	def setUp(self):
		Candidate.objects.create(
				email='email@example.com',
				first_name='John',
				last_name='Doe',
				citizenship='Antarctica',
				timezone='Antarctica',
				date_of_birth=datetime.date(1970, 1, 1)
			)

	def test_candidate_creation(self):
		candidate = Candidate.objects.get(first_name='John')
		self.assertEqual(candidate.email, 'email@example.com')
		self.assertEqual(candidate.first_name, 'John')