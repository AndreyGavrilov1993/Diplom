from django.test import TestCase

# Create your tests here.
from .models import CartItem, Product
import pdb; pdb.set_trace()

class ProductTest(TestCase):
    def test_str_method(self):
        obj = Product(name="Test")
        self.assertEqual(str(obj), "Test")

class CartItemTest(TestCase):
    def test_str_method(self):
        obj = CartItem(name="Test")
        self.assertEqual(str(obj), "Test")