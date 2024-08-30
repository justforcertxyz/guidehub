from django.test import TestCase
from .models import Inquiry

class InquiryModelTest(TestCase):
    def test_inquiry_model_exists(self):
        inquiry_count = Inquiry.objects.count()

        self.assertEqual(inquiry_count, 0)    
