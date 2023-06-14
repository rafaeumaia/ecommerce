from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Name', null=True)
    email = models.EmailField(max_length=200, verbose_name='Email', null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    price = models.FloatField(verbose_name='Price')
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Image')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Customer')
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name='Date Ordered')
    complete = models.BooleanField(default=False, null=True, blank=False, verbose_name='Complete')
    transaction_id = models.CharField(max_length=100, null=True, verbose_name='Transaction Id')

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.total for item in orderitems])
        return total

    @property
    def cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Product')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Order')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Quantity')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date Added')

    @property
    def total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Customer')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Order')
    address = models.CharField(max_length=200, null=False, verbose_name='Address')
    city = models.CharField(max_length=200, null=False, verbose_name='City')
    state = models.CharField(max_length=200, null=False, verbose_name='State')
    zipcode = models.CharField(max_length=200, null=False, verbose_name='ZipCode')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date Added')

    def __str__(self):
        return self.address
