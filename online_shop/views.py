from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Products, Photos

class ProductsList(View):
    def get(self, request):
        products = Products.objects.all()
        photos = []
        for product in products:
            for url in product.photo.all():                    # dodawać co 3 zdjęcie?
                photos.append(url.image_urls)
        ctx = {
            'photos': photos,
            'products': products
        }

        return render(request, 'index.html', ctx)


# class AccountOrders(View):
#     def get(self, request):
#         pass
#         return render(request, 'account-orders.html')


class OrdersBasket(View):
    def get(self, request):
        pass
        return render(request, 'cart.html')


class ProductDetails(View):
    def get(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        photos = product.photo.all()

        ctx = {
            'product': product,
            'photos': photos
        }
        return render(request, 'shop-single.html', ctx)