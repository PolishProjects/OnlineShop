# Generated by Django 2.0.2 on 2018-03-05 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0007_auto_20180305_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='products',
        ),
        migrations.AddField(
            model_name='photos',
            name='products',
            field=models.ManyToManyField(null=True, related_name='photo', to='online_shop.Products'),
        ),
    ]