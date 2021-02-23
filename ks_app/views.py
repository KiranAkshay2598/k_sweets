from django.shortcuts import render, redirect
from .models import *
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from .services import send_telegram_message, razorpay_gateway, init_cookie

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
        response = render(request, 'index.html', context=category_context)
        if not 'order_id' in request.COOKIES:
            new_order = Order.objects.create()
            response.set_cookie("order_id", new_order.id)
        return response


class CategoryView(View):
    def get(self, request):
        if len(request.GET) == 0:
            products=Product.objects.all()
            all_category = Category.objects.all()
            order=Order.objects.get(id=request.COOKIES['order_id'])
            cart_items=order.cart_item.all()
            context = {
            'products' : products,
            'all_category' : all_category,
            'cart_items' : cart_items
            }
            return render(request,'shop.html',context=context)


        elif len(request.GET) == 1:
            cat_name = request.GET["cat_name"]
            print(len(request.GET))
            all_category = Category.objects.all()
            category = Category.objects.get(name=cat_name)
            products = category.product_set.all()
            order=Order.objects.get(id=request.COOKIES['order_id'])
            cart_items=order.cart_item.all()
            context = {
            'products' : products,
            'all_category' : all_category,
            'cart_items':cart_items
            }   
            return render(request,'shop.html',context=context)


        elif len(request.GET) == 3:
            cat_name = request.GET["cat_name"]
            prc_frm = request.GET["prc_frm"]
            prc_to = request.GET["prc_to"]
            if cat_name:
                category = Category.objects.get(name=cat_name)    
                products = category.product_set.filter(price__gte = prc_frm, price__lte = prc_to)
            else:
                products = Product.objects.filter(price__gte = prc_frm, price__lte = prc_to)
         
        if len(request.GET) > 1:
            products_list = []
            for product in products:
                products_list.append(product.id)
            return JsonResponse({
                'filtered_products' : products_list
            })
        # return HttpResponse("Testing if recieving id " + str(cat_id))
    def post(self,request):
        search_query = request.POST["search_query"]
        all_category = Category.objects.all()
        order=Order.objects.get(id=request.COOKIES['order_id'])
        cart_items=order.cart_item.all()
        products = Product.objects.filter(name__icontains=search_query)
        
        context = {
            'products' : products,
            'all_category' : all_category,
            'cart_items':cart_items
            } 
        return render(request,'shop.html',context=context)


class AddItemToOrder(View):
    def post(self, request):
        product_id=int(request.POST["product_id"])
        qty=int(request.POST["quantity"])
        cart_item_to_add = CartItem.objects.create(product_id=product_id,qty=qty) 
        order = Order.objects.get(id=request.COOKIES['order_id'])
        order.cart_item.add(cart_item_to_add)
        order.save()
        return HttpResponse("added item to cart")


class OrderView(View):
    def get(self, request):
        order=Order.objects.get(id=request.COOKIES['order_id'])
        cart_items=order.cart_item.all()
        context = {
            'cart_items':cart_items
        }
        return render(request,'cart.html',context=context)

    def post(self, request):
        data_list = request.POST
        if 'remove_button' in data_list.keys():
            id = data_list['cartitem_id']
            cart_item = CartItem.objects.get(id=int(id))
            cart_item.delete()
            return HttpResponse("removed successfully")


        else:
            updated_total = dict()
            for key, value in data_list.items():
                if key.find('qtybox') != -1:
                    id = key.replace('qtybox','')
                    qty = int(value)
                    cart_item = CartItem.objects.get(id=int(id))
                    if qty != cart_item.qty:
                        cart_item.qty = qty
                        cart_item.save()
                        item_total = cart_item.qty * cart_item.product.price
                        updated_total[cart_item.id] = item_total
            return JsonResponse(updated_total)

class CheckoutOrder(View): #checkout url view
    def get(self, request):
        order=Order.objects.get(id=request.COOKIES['order_id'])
        cart_items=order.cart_item.all()
        context = {
            'cart_items':cart_items
        }
        return render(request, 'checkout.html', context=context)

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
            customer_name = order.customer_name
            phone_number = order.phone_number
            email = order.email
            address = order.address
            for cart_item in all_cart_items:
                qty = cart_item.qty
                price = cart_item.product.price
                qty_price = qty * price
                total += qty_price
                name = cart_item.product.name
                msg += "PRODUCT NAME - " + name + " QTY - " + str(qty) + "QTY PRICE" + str(qty_price) + "\n"
            msg += "TOTAL BILL : " + str(total) + "\n PHONE NUMBER : " + phone_number + "\n EMAIL ID : "  +  email +  "\n ADDRESS : " +  address 
            rpay_oid = razorpay_gateway(total*100)
            send_telegram_message(msg)
            response = render(request, 'pay.html', context={"rpay_oid":rpay_oid})
            response.delete_cookie('order_id')
            new_order = Order.objects.create()
            response.set_cookie("order_id", new_order.id)
            return response
        except Exception as e:
            return HttpResponse("Failure")

class SuccessRedirect(View):
    def get(self, request):
        return render(request, "success_pay.html")


class About_us(View):
    def get(self,request):
        order=Order.objects.get(id=request.COOKIES['order_id'])
        cart_items=order.cart_item.all()
        context = {
            'cart_items':cart_items
        }
        return render(request,'about.html',context=context)


class Shop_detail(View):
    def get(self,request):
        return render(request,"shop-detail.html")


# class Cart(View):
#     def get(self,request):
#         return render(request,"cart.html")


class Checkout(View):
    def get(self,request):
        return render(request,"checkout.html")

        
