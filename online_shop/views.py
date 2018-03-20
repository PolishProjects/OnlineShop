from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product, ShippingOption, Order, User
from django.http import QueryDict


class MainPage(View):
    def get(self, request):
        products = Product.objects.all()
        photos = []
        for product in products:
            for url in product.photo.all():
                photos.append(url.image_urls)

        if 'basket' in request.session.keys():
            ctx = {
                'photos': photos,
                'products': products,
                'products_amount': request.session['basket']
            }

            return render(request, 'index.html', ctx)
        else:
            ctx = {
                'photos': photos,
                'products': products,
            }

            return render(request, 'index.html', ctx)


# class AccountOrders(View):
#     def get(self, request):
#         pass
#         return render(request, 'account-orders.html')


class Basket(View):
    def get(self, request):
        products = []
        if 'basket' in request.session.keys():                       # zapisać products_amount w context processor (cena się wyświetla w buttonie koszyka)
            products_id = request.session['basket']
            for id in products_id:
                products.append(Product.objects.get(pk=id))

            ctx = {
                'products': list(set(products)),
                'products_amount': request.session['basket']
            }
            return render(request, 'basket.html', ctx)
        else:
            ctx = {
                'products': products
            }
            return render(request, 'basket.html', ctx)

    def post(self, request):
        products = request.session.get('basket', {})

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product_amount = request.POST.get('product_amount')
            products[product_id] = product_amount
            request.session['basket'] = products

        return render(request, 'basket.html')

    def delete(self, request):
        remove_id_product = QueryDict(request.body).get('product_id')

        for id in list(request.session['basket'].keys()):
            if remove_id_product == id:
                del request.session['basket'][id]

        request.session.modified = True

        return render(request, 'basket.html')

    def put(self, request):
        product_amount = QueryDict(request.body).get("product_amount")
        product_id = QueryDict(request.body).get("product_id")

        if product_id in request.session['basket'].keys():
            del request.session['basket'][product_id]

        products_amount = request.session.get('basket', {})
        products_amount[product_id] = product_amount
        request.session['basket'] = products_amount

        return render(request, 'basket.html')


class ClearBasket(View):
    def get(self, request):
        request.session.clear()
        return redirect('/basket')


class ProductDetails(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        photos = product.photo.all()

        ctx = {
            'product': product,
            'photos': photos
        }
        return render(request, 'shop-single.html', ctx)


class ShowAllProducts(View):
    def get(self, request):
        products = Product.objects.all()

        ctx = {
            'products': products
        }
        return render(request, 'shop-grid-ns.html', ctx)

class CheckoutAddress(View):
    def get(self, request):
        return render(request, 'checkout-address.html')

    def post(self, request):
        order = request.session.get('order', {})

        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone_number')
            company = request.POST.get('company')
            country = request.POST.get('country')
            city = request.POST.get('city')
            postal_code = request.POST.get('postal_code')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')

            order['first_name'] = first_name
            order['last_name'] = last_name
            order['email'] = email
            order['phone_number'] = phone
            order['company'] = company
            order['country'] = country
            order['city'] = city
            order['postal_code'] = postal_code
            order['address1'] = address1
            order['address2'] = address2

            request.session['order'] = order

        return render(request, 'checkout-address.html')


class CheckoutShipping(View):
    def get(self, request):
        shipping_options = ShippingOption.objects.all()

        ctx = {
            'shipping_options': shipping_options
        }

        return render(request, 'checkout-shipping.html', ctx)

    def post(self, request):
        shipping_method = request.session.get('shipping_method', {})

        if request.method == 'POST':
            shipping_method_id = request.POST.get('shipping_method_id')
            shipping_method['shipping_method_id'] = shipping_method_id

            request.session['shipping_method'] = shipping_method

        return render(request, 'checkout-shipping.html')


class CheckoutReview(View):
    def get(self, request):
        products = []
        if 'basket' in request.session.keys():
            product_ids = request.session['basket']
            for id in product_ids:
                products.append(Product.objects.get(pk=id))

            ctx = {
                'products': list(set(products)),
                'products_amount': request.session['basket']
            }

            return render(request, 'checkout-review.html', ctx)
        else:
            return render(request, 'checkout-review.html')


class CheckoutComplete(View):
    def get(self, request):
        product_ids = request.session['basket'].keys()
        order = request.session['order']
        shipping_option = ShippingOption.objects.get(pk=request.session['shipping_method']['shipping_method_id'])

        user = User(first_name=order['first_name'], last_name=order['last_name'], e_mail=order['email'],
                    phone_number=order['phone_number'], company=order['company'], country=order['country'],
                    city=order['city'], postal_code=order['postal_code'], address1=order['address1'],
                    address2=order['address2'])
        user.save()

        make_order = Order(user=user)
        make_order.save()

        for id in product_ids:
            for product in Product.objects.filter(pk=id):
                make_order.products.add(product)

        make_order.shipping_options.add(shipping_option)

        return render(request, 'checkout-complete.html')