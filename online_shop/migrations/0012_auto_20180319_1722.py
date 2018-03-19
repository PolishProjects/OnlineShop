# Generated by Django 2.0.3 on 2018-03-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0011_auto_20180319_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_options',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_options',
            field=models.ManyToManyField(related_name='orders_shipping_option', to='context_processor.ShippingOption'),
        ),
    ]
