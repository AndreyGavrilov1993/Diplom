from django.test import TestCase

# Create your tests here.
from .models import Feedback
import pdb; pdb.set_trace()

class FeedbackTest(TestCase):
    def test_str_method(self):
        obj = Feedback(name="Test")
        self.assertEqual(str(obj), "Test")