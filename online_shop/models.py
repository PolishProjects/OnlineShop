from django.db import models
from django.core.validators import URLValidator


class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=256, null=True)

    def __str__(self):
        return '{}/{} sth.'.format(self.name, self.stock)


class Photo(models.Model):
    image_urls = models.TextField(validators=[URLValidator()], null=True)
    products = models.ManyToManyField(Product, related_name='photo')

    def __str__(self):
        products = []
        for product in self.products.all():
            products.append(product.name)
        return ' - '.join(products)


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)          # validation
    e_mail = models.CharField(max_length=64)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_user')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='orders_product')