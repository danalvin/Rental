from django.test import TestCase
from django.urls import reverse

from .models import Tenant

class TenantModelTestCase(TestCase):
    def setUp(self):
        Tenant.objects.create(
            First_name="John",
            Second_name="Doe",
            ID_numnber="1234567890",
            phone_number="1234567890"
        )

    def test_tenant_creation(self):
        tenant = Tenant.objects.get(first_name="John")
        self.assertEqual(str(tenant), "John Doe")
        
    def test_tenant_list_view(self):
        response = self.client.get(reverse('tenant_list'))
        self.assertEqual(response.status_code, 200)
        
    def test_tenant_detail_view(self):
        tenant = Tenant.objects.get(first_name="John")
        response = self.client.get(reverse('tenant_detail', args=[tenant.id]))
        self.assertEqual(response.status_code, 200)
