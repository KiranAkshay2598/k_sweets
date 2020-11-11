from django.urls import path
from . import views

urlpatterns = [
    path('home',views.HomeView.as_view(), name='home'),
    path('category',views.CategoryView.as_view(), name='category'),
    path('update-order',views.UpdateOrder.as_view(), name='update-order'),
    path('add-item', views.AddItemToOrder.as_view(), name='add-item'),
    path('send-order', views.SendOrder.as_view(), name='send-order'),
    path('success-pay', views.SuccessRedirect.as_view(), name='success-pay'),
]