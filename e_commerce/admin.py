from django.contrib import admin
from .models import User, Item, Cart, FavList, Order

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(FavList)
# admin.site.register(Shipping)
admin.site.register(Order)