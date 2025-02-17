from telnetlib import STATUS
from django.db import models
from django.contrib.auth.models import AbstractUser


# ========== User Model ========== #
class User(AbstractUser):
   name = models.CharField(max_length=150, null=True)
   username = models.CharField(unique= True, max_length=50, null=True)
   email = models.EmailField(max_length=150, null=True)
   
   USERNAME_FIELD = 'username'


# ========== Item Model ========== #
class Item(models.Model):
   cart_id = models.IntegerField(default=0, null=True)
   creator_id = models.IntegerField(default=0, null=True)
   fav_id = models.IntegerField(default=0, null=True)
   product_id = models.IntegerField(default=0, null=True)
   name = models.CharField(max_length=150, default='item')
   image = models.CharField(max_length=200, default='image')
   price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
   quantity = models.IntegerField(default=0)

   def calc_price(self):
      return self.price * self.quantity

   def __str__(self):
      return self.name


# ========== Cart Model ========== #
class Cart(models.Model):
   cart_id = models.IntegerField(default=0, null=True)
   name = models.CharField(max_length=10, default='cart')
   item = models.ManyToManyField(Item)

   def __str__(self):
      return self.name


# ========== Cart Model ========== #
class FavList(models.Model):
   favList_id = models.IntegerField(default=0, null=True)
   name = models.CharField(max_length=10, default='favList')
   item = models.ManyToManyField(Item)

   def __str__(self):
      return self.name


# ========== Shipping Model ========== #
# class Shipping(models.Model):
#    ship_id = models.IntegerField(default=0, null=True)
#    name = models.CharField(max_length=10)
#    email = models.EmailField(max_length=150, null=True)
#    address_1 = models.CharField(max_length=1024)
#    address_2 = models.CharField(max_length=1024)
#    zip_code = models.CharField(max_length=10, null=True)
#    city = models.CharField(max_length=150)
#    country = models.CharField(max_length=50)

#    def __str__(self):
#       return self.name


# ========== Order Model ========== #
class Order(models.Model):
   name = models.CharField(max_length=150, default='order_')
   customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
   amount = models.DecimalField(default=0, decimal_places=2, max_digits=6)
   # shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True)
   PENDING = 'pending'
   DELIVERING = 'out for delivery'
   DELIVERED = 'delivered'
   STATUS = (
      (PENDING,'pending'),
      (DELIVERING,'out for delivery'),
      (DELIVERED,'delivered')
   )
   status = models.CharField(max_length=20, choices=STATUS, default=PENDING)

   def __str__(self):
      return self.name