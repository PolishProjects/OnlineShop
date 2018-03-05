from django.db import models
from django.core.validators import URLValidator


class Products(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image_urls = models.TextField(validators=[URLValidator()], null=True)
    description = models.CharField(max_length=256, null=True)

    def __str__(self):
        return '{}/{} EUR'.format(self.name, self.price)

# class Photos(models.Model):
#     photos = models.ForeignKey(Products, on_delete=models.CASCADE)


class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)          # validation
    e_mail = models.CharField(max_length=64)


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)