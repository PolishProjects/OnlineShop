# Generated by Django 2.0.2 on 2018-03-05 20:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0003_auto_20180305_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='image_urls',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='online_shop.Products', validators=[django.core.validators.URLValidator()]),
        ),
    ]