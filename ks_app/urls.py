from django.urls import path
from . import views

urlpatterns = [
    path('home',views.HomeView.as_view(), name='home'),
    path('category',views.CategoryView.as_view(), name='category'),
    path('update-order',views.CheckoutOrder.as_view(), name='update-order'),
    path('add-item', views.AddItemToOrder.as_view(), name='add-item'),
    path('send-order', views.SendOrder.as_view(), name='send-order'),
    path('success-pay', views.SuccessRedirect.as_view(), name='success-pay'),
    path('about-us', views.About_us.as_view(), name='about-us'),
    path('shop-detail', views.Shop_detail.as_view(), name='shop-detail'),
    path('cart', views.OrderView.as_view(), name='cart'),
    path('checkout', views.Checkout.as_view(), name='checkout')
]