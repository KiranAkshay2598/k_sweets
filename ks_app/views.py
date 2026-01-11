from django.shortcuts import render, redirect
from .models import *
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from .services import send_telegram_message, razorpay_gateway, init_cookie

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
        order_id = request.COOKIES.get('order_id')
        cart_items = []
        if order_id:
             try:
                 order = Order.objects.get(id=order_id)
                 cart_items = order.cart_item.all()
             except Order.DoesNotExist:
                 pass
        
        if len(request.GET) == 0:
            products=Product.objects.all()
            all_category = Category.objects.all()
            context = {
            'products' : products,
            'all_category' : all_category,
            'cart_items': cart_items
            }
            return render(request,'shop.html',context=context)


        elif 'cat_name' in request.GET and 'prc_frm' not in request.GET: # Category-only filtering
            cat_name = request.GET.get("cat_name")
            
            all_category = Category.objects.all()
            if cat_name:
                try:
                    category = Category.objects.get(name=cat_name)
                    products = category.product_set.all()
                except Category.DoesNotExist:
                    products = Product.objects.none()
            else:
                 products = Product.objects.all()

            context = {
            'products' : products,
            'all_category' : all_category,
            'cart_items':cart_items,
            'active_category': cat_name
            }   
            return render(request,'shop.html',context=context)


        elif 'prc_frm' in request.GET: # Price filtering (likely AJAX)
            cat_name = request.GET.get("cat_name")
            prc_frm = request.GET.get("prc_frm")
            prc_to = request.GET.get("prc_to")
            
            # Convert null string to None if coming from JS
            if cat_name == 'null' or cat_name == 'None': 
                cat_name = None

            if cat_name:
                try:
                    category = Category.objects.get(name=cat_name)    
                    products = category.product_set.filter(price__gte = prc_frm, price__lte = prc_to)
                except Category.DoesNotExist:
                    products = Product.objects.filter(price__gte = prc_frm, price__lte = prc_to)
            else:
                products = Product.objects.filter(price__gte = prc_frm, price__lte = prc_to)
         
        if len(request.GET) > 1:
            products_list = []
            for product in products:
                products_list.append(product.id)
            return JsonResponse({
                'filtered_products' : products_list
            })

    def post(self,request):
        search_query = request.POST["search_query"]
        all_category = Category.objects.all()
        
        cart_items = []
        try:
             order=Order.objects.get(id=request.COOKIES.get('order_id'))
             cart_items=order.cart_item.all()
        except (Order.DoesNotExist, TypeError):
             pass

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
        
        order_id = request.COOKIES.get('order_id')
        order = None
        
        if order_id:
             try:
                 order = Order.objects.get(id=order_id)
             except Order.DoesNotExist:
                 order = None

        if not order:
             order = Order.objects.create()

        existing_item = order.cart_item.filter(product__id=product_id).first()
        if existing_item:
            existing_item.qty += qty
            existing_item.save()
        else:
            cart_item_to_add = CartItem.objects.create(product_id=product_id,qty=qty) 
            order.cart_item.add(cart_item_to_add)
            
        order.save()
             
        response = HttpResponse("added item to cart")
        if not order_id or str(order.id) != str(order_id):
            response.set_cookie("order_id", order.id)
            
        return response


class OrderView(View):
    def get(self, request):
        order_id = request.COOKIES.get('order_id')
        cart_items = []
        if order_id:
             try:
                 order=Order.objects.get(id=order_id)
                 cart_items=order.cart_item.all()
             except Order.DoesNotExist:
                 pass
        
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
        order_id = request.COOKIES.get('order_id')
        cart_items = []
        if order_id:
             try:
                 order=Order.objects.get(id=order_id)
                 cart_items=order.cart_item.all()
             except Order.DoesNotExist:
                 pass
        
        context = {
            'cart_items':cart_items
        }
        return render(request, 'checkout.html', context=context)

    def post(self, request):
        try:
            val = request.COOKIES.get('order_id')
            if not val:
                 return HttpResponse("Order ID not found in cookies")
            order = Order.objects.get(id=val)
            order.customer_name = request.POST["customer_name"]
            order.phone_number = request.POST["phone_number"]
            order.email = request.POST["email"]
            order.address = request.POST["address"]
            order.save()
            return HttpResponse("Order updated successfully")
        except Exception as e:
            return HttpResponse(f"failure: {e}")


class SendOrder(View):
    def get(self, request):
        try:
            total = 0
            order_id = request.COOKIES.get('order_id')
            if not order_id:
                 return redirect('home')

            order = Order.objects.get(id=order_id)
            msg = "🛍️ NEW ORDER RECEIVED\n"
            msg += "👤 Customer: " + str(order.customer_name) + "\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            all_cart_items = order.cart_item.all()
            phone_number = str(order.phone_number)
            email = str(order.email)
            address = str(order.address)
            
            for i, cart_item in enumerate(all_cart_items, 1):
                qty = cart_item.qty
                price = cart_item.product.price
                qty_price = qty * price
                total += qty_price
                name = cart_item.product.name
                msg += str(i) + ". " + name + "\n"
                msg += "   Qty: " + str(qty) + "  |  Amt: Rs." + str(qty_price) + "\n\n"
            
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            msg += "💰 TOTAL BILL : Rs." + str(total) + "\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            msg += "📍 DELIVERY DETAILS\n"
            msg += "📞 Phone   : " + phone_number + "\n"
            msg += "📧 Email   : " + email + "\n"
            msg += "🏠 Address : " + address 
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
        order_id = request.COOKIES.get('order_id')
        cart_items = []
        if order_id:
             try:
                 order=Order.objects.get(id=order_id)
                 cart_items=order.cart_item.all()
             except Order.DoesNotExist:
                 pass
        
        context = {
            'cart_items':cart_items
        }
        return render(request,'about.html',context=context)


class Shop_detail(View):
    def get(self,request):
        return render(request,"shop-detail.html")


class Checkout(View):
    def get(self,request):
        return render(request,"checkout.html")

        
