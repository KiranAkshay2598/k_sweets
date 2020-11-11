from django.db import models
from .constants import unit_choices

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, default=None, null=True, choices=unit_choices)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)      

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)
    qty = models.IntegerField()

    def __str__(self):
        return self.product.name + " item"

class Order(models.Model):
    cart_item = models.ManyToManyField(CartItem)
    customer_name = models.CharField(max_length=300, null=True, default=None)
    phone_number = models.CharField(max_length=10, null=True, default=None)
    email = models.CharField(max_length=300, null=True, default=None)
    address = models.CharField(max_length=1000, null=True, default=None)

    # def __str__(self):
    #     return self.customer_name + "'s order"

