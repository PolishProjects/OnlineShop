# Generated by Django 2.0.3 on 2018-03-19 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0010_auto_20180307_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_method', models.CharField(max_length=64)),
                ('available_destinations', models.CharField(max_length=64)),
                ('delivery_time', models.CharField(max_length=64)),
                ('delivery_size', models.CharField(max_length=64)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_options',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_shipping_option', to='online_shop.ShippingOptions'),
        ),
    ]
