# Generated by Django 2.0.2 on 2018-03-05 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0005_auto_20180305_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='online_shop.Products'),
        ),
    ]