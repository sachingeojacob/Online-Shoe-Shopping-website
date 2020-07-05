from datetime import datetime

from django.db import models


class Login(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class User(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    gender = models.CharField(max_length=20)
    isapprove = models.BooleanField(default=True)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return self.fname


class Product(models.Model):
    productname = models.CharField(max_length=1000)
    brandname = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    producttype = models.CharField(max_length=100)
    quantity = models.IntegerField(default=10)
    size = models.IntegerField(default=3)
    image = models.ImageField()

    def __str__(self):
        return self.productname


class Cart(models.Model):
    prd_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    cart_date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.user_id


class Booking(models.Model):
    user_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    totalprice = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Packing')

    def __str__(self):
        return self.status




class Bookingitem(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.booking_id


class BookingAddress(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    state = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.email
