from django.test import TestCase
from django.urls import reverse

from .models import Occupation
from datetime import date, timedelta


class OccupationModelTestCase(TestCase):
    def setUp(self):
        Occupation.objects.create(
            tenant_first_name="John Doe",
            house_name="House 1",
            start_date=date.today() - timedelta(days=30),
            rent_amount=15000,
            rent_due_date=date.today() + timedelta(days=7)
        )

    def test_occupation_creation(self):
        occupation = Occupation.objects.get(tenant_first_name="John Doe")
        self.assertEqual(str(occupation), "John Doe - House 1")
        
    def test_occupation_list_view(self):
        response = self.client.get(reverse('occupation_list'))
        self.assertEqual(response.status_code, 200)
        
    def test_occupation_detail_view(self):
        occupation = Occupation.objects.get(tenant_first_name="John Doe")
        response = self.client.get(reverse('occupation_detail', args=[occupation.id]))
        self.assertEqual(response.status_code, 200)
