from django.test import TestCase

# Create your tests here.
from .models import User
import pdb; pdb.set_trace()

class UserTest(TestCase):
    def test_str_method(self):
        obj = User(name="Test")
        self.assertEqual(str(obj), "Test")