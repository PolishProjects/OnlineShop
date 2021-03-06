$(document).ready(function() {

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');


      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    var product_in_basket = [];
    $(".add_to_basket").click(function () {
        var product_id = this.id;
        var display_quantity_products = $('.display-quantity-products');
        var total_basket_price = $('.total-basket-price');
        var dropdown_basket_price = $('.dropdown-basket-price');
        var display_price_basket = 0;
        var products_in_basket = eval(display_quantity_products.data('value'));

        // Quantity all products and total price in button
        if($.inArray(product_id, product_in_basket) === -1) {
            product_in_basket.push(product_id);
            if($.inArray(product_id, products_in_basket) === -1) {
                display_quantity_products.text(parseInt(display_quantity_products.text()) + 1);
                display_price_basket += parseFloat(this.name);
            }
        }

        dropdown_basket_price.text((parseFloat(total_basket_price.text()) + parseFloat(display_price_basket)).toFixed(2) + ' EUR');
        total_basket_price.text((parseFloat(total_basket_price.text()) + parseFloat(display_price_basket)).toFixed(2) + ' EUR');


        $.ajax({
            type: "POST",
            url: "/basket/",
            data: {
                'product_id': this.id,
                'quantity_product': 1
            }
        });
    });


    $('.quantity_products').change(function () {
        var product_id = this.id;
        var quantity_product = this.value;
        var price_per_product = this.dataset.inlineType;

        // Subtotal product price in basket and dropdown
        var dropdown_product_price = $('.dropdown-product-price');
        var subtotal_product_price = $('.subtotal-product-price');
        $.each(subtotal_product_price, function (index, subtotal_product_price) {
            if (product_id === subtotal_product_price.id) {
                subtotal_product_price.innerHTML = (parseFloat(quantity_product) * parseFloat(price_per_product)).toFixed(2) + ' EUR';

                $.each(dropdown_product_price, function (index, value) {
                    if (product_id === value.id) {
                        value.innerHTML = (parseFloat(price_per_product) * parseInt(quantity_product)).toFixed(2);
                    }
                });
            }
        });

        // Total products price in basket and dropdown
        var dropdown_basket_price = $('.dropdown-basket-price');
        var total_basket_price = $('.total-basket-price');
        var summary_price = 0;
        var quantity_product_selected = $('.quantity_products option:selected');
        $.each(quantity_product_selected, function (index, value) {
            summary_price += parseFloat(value.value * value.id);
        });

        total_basket_price.text((summary_price).toFixed(2) + ' EUR');
        dropdown_basket_price.text((summary_price).toFixed(2) + ' EUR');

        // Quantity product in dropdown
        var dropdown_product_quantity = $('.dropdown-product-quantity');
        $.each(dropdown_product_quantity, function (index, value) {
            if (product_id === value.id) {
                value.innerHTML = quantity_product;
            }
        });


        $.ajax({
            type: "PUT",
            url: "/basket/" + product_id,
            data: {
                'product_id': product_id,
                'quantity_product': quantity_product
            }
        });
    });

    // Removing product from basket and dropdown
    $('.remove-from-cart, .dropdown-product-remove').click(function () {
        var basket_selected_product = $('.basket-selected-product');
        var dropdown_selected_product = $('.dropdown-selected-product');
        var review_selected_product = $('.review-selected-product');

        var product_id = this.id;
        var display_quantity_products = $('.display-quantity-products');

        var total_basket_price = $('.total-basket-price');


        // Subtotal product price in basket and dropdown
        var subtotal_product_price = 0;
        var quantity_product_selected = $('.quantity_products option:selected');
        $.each(quantity_product_selected, function (index, value) {
            if(value.dataset.inlineType === product_id) {
                subtotal_product_price += parseFloat(value.value * value.id);
            }
        });


        // Removing product from basket
        var basket_total_price = 0;
        $.each( basket_selected_product, function(index, value) {
            if (product_id === value.id) {
                basket_total_price += parseInt(total_basket_price.text()) - parseInt(subtotal_product_price);
                value.remove();
            }
        });

        // Removing product from order review
        var dropdown_product_price = 0;
        var dropdown_product = $('.dropdown-product-price');
        $.each( dropdown_product, function(index, value) {
            if (product_id === value.id) {
                dropdown_product_price += parseInt(value.innerHTML);
            }
        });

        // Removing product from order review
        var dropdown_total_price = 0;
        $.each( dropdown_selected_product, function(index, value) {
            if (product_id === value.id) {
                dropdown_total_price += parseInt(total_basket_price.text()) - parseInt(dropdown_product_price);
                value.remove();
            }
        });

        // Removing product from dropdown
        var review_total_price = 0;
        $.each( review_selected_product, function(index, value) {
            if (product_id === value.id) {
                review_total_price += parseInt(total_basket_price.text()) - parseInt(dropdown_product_price);
                value.remove();
            }
        });

        display_quantity_products.text(parseInt(display_quantity_products.text()) - 1);


        total_basket_price.text((basket_total_price).toFixed(2) + ' EUR');
        total_basket_price.text((dropdown_total_price).toFixed(2) + ' EUR');
        $('.dropdown-basket-price').text((dropdown_total_price).toFixed(2) + ' EUR');
        $('.shipping-total').text((dropdown_total_price + parseFloat($('.shipping-cost').text())).toFixed(2) + ' EUR');
        $('.review-total-cost').text((review_total_price + parseFloat($('.shipping-cost').text())).toFixed(2) + ' EUR');

        $.ajax({
            type: "DELETE",
            url: "/basket/" + product_id,
            data: {
                "product_id": product_id
            }
        });
    });

    // Shipping in order summary
    $(".shipping-method").focus(function() {
        var shipping_id = this.value;
        var shipping_price = $(".shipping-price");
        var basket_price = $('.total-basket-price').html();
        var order_summary_price = $('.shipping-total');

        var selected_shipping_price = 0;
        $.each(shipping_price, function(index, value) {
            if (shipping_id === this.id) {
                selected_shipping_price += parseInt(value.dataset.inlineType);
                $('.shipping-cost').html((parseFloat(value.dataset.inlineType)).toFixed(2) + ' EUR');
            }
        });
        order_summary_price.html((parseInt(basket_price) + selected_shipping_price).toFixed(2) + ' EUR')
    });
});