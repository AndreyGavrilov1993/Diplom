# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta

import stripe

stripe.api_key = "your_stripe_secret_key"

def get_available_datetime():
    """
    Возвращает доступные дату и время для заказа.
    """
    # Получаем текущую дату и время
    now = datetime.now()

    # Устанавливаем минимальный интервал для заказа (например, 1 час)
    min_interval = timedelta(hours=1)

    # Округляем время до ближайшего интервала
    available_time = now + min_interval
    available_time = available_time.replace(minute=0, second=0, microsecond=0)

    # Возвращаем доступные дату и время
    return available_time.date(), available_time.time()

class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(null=True)
	quantity = models.PositiveIntegerField(default=0)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='products/')

	def __str__(self):
		return self.name

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
	payment_status = models.CharField(max_length=50, default="unpaid")
	date_added = models.DateTimeField(auto_now_add=True)
	order_day, order_time = get_available_datetime()

	def __str__(self):
		return f'{self.quantity} x {self.product.name}'

	def get_total_price(self):
		return self.quantity * self.product.price

	def create_payment_intent(self):
		payment_intent = stripe.PaymentIntent.create(
			amount=int(self.total_price * 100),
			currency="usd",
			payment_method_types=["card"],
		)
		self.payment_intent_id = payment_intent.id
		self.save()
		return payment_intent.client_secret

	def update_payment_status(self, payment_status):
		self.payment_status = payment_status
		self.save()


	class Meta:
		verbose_name = 'Заказ аренды'
		verbose_name_plural = 'Заказы аренды'