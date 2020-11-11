from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.http import HttpResponse
from .services import send_telegram_message, razorpay_gateway

# def home(request):
#     if request.method == "GET":
#         categories = Category.objects.all()
#         category_context = {
#             'all_categories' : categories
#         }
#         return render(request, 'home.html', context=category_context)

class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_context = {
            'all_categories' : categories
        }
        response = render(request, 'home.html', context=category_context)
        if not 'order_id' in request.COOKIES:
            new_order = Order.objects.create()
            response.set_cookie("order_id", new_order.id)
        return response
class CategoryView(View):
    def get(self, request):
        cat_name = request.GET["cat_name"]
        category = Category.objects.get(name=cat_name)
        products = category.product_set.all()
        context = {
            'products' : products
        }
        return render(request,'category.html',context=context)
        # return HttpResponse("Testing if recieving id " + str(cat_id))


class AddItemToOrder(View):
    def post(self, request):
        product_id=int(request.POST["product_id"])
        qty=int(request.POST["quantity"])
        cart_item_to_add = CartItem.objects.create(product_id=product_id,qty=qty) 
        order = Order.objects.get(id=request.COOKIES['order_id'])
        order.cart_item.add(cart_item_to_add)
        order.save()
        return HttpResponse("added item to cart")


class UpdateOrder(View):
    def get(self, request):
        return render(request, 'create-cart.html')

    def post(self, request):
        try:
            order = Order.objects.get(id=request.COOKIES['order_id'])
            order.customer_name = request.POST["customer_name"],
            order.phone_number = request.POST["phone_number"],
            order.email = request.POST["email"],
            order.address = request.POST["address"]
            order.save()
            return redirect('send-order')
        except Exception as e:
            return HttpResponse("failure")


class SendOrder(View):
    def get(self, request):
        try:
            total = 0
            order = Order.objects.get(id=request.COOKIES['order_id'])
            msg = " These are the orders from " + order.customer_name + "\n"
            all_cart_items = order.cart_item.all()
            for cart_item in all_cart_items:
                qty = cart_item.qty
                price = cart_item.product.price
                qty_price = qty * price
                total += qty_price
                name = cart_item.product.name
                msg += "PRODUCT NAME - " + name + " QTY - " + str(qty) + "QTY PRICE" + str(qty_price) + "\n"
            msg += "TOTAL BILL : " + str(total) 
            rpay_oid = razorpay_gateway(total*100)
            send_telegram_message(msg)
            return render(request, 'pay.html', context={"rpay_oid":rpay_oid})
        except Exception as e:
            return HttpResponse("Failure")

class SuccessRedirect(View):
    def get(self, request):
        return render(request, "success_pay.html")