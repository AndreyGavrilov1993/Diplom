# Generated by Django 4.2.7 on 2024-07-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_cartitem_order_day_remove_cartitem_order_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='payment_status',
            field=models.CharField(default='unpaid', max_length=50),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
