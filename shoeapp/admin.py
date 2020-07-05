from django.contrib import admin
from .models import Login, User, Product, Cart, Booking, Bookingitem, BookingAddress

# Register your models here.


admin.site.register(Login)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Booking)
admin.site.register(Bookingitem)
admin.site.register(BookingAddress)
