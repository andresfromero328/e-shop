from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from datetime import datetime
from .forms import UserRegistration
from .models import FavList, Order, User, Item, Cart
from django.contrib import messages
import requests


# ========== Register View ========== #
def registerPage(request):
   form = UserRegistration()
   context = {'form': form}

   if request.method == 'POST':
      form = UserRegistration(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, 'Registration phase encountered an error')


   context = {'form': form}
   return render(request, 'login-register.html', context)


# ========== Login View ========== #
def loginPage(request):
   page = 'login'

   if request.user.is_authenticated:
      return redirect('home')
   
   if request.method == 'POST':
      username = request.POST.get('username').lower()
      psw = request.POST.get('password')

      try:
         user = User.objects.get(username=username)
      except:
         messages.error(request, 'Username does not exist')
      
      user = authenticate(request, username=username, password=psw)
      if user is not None:
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, 'Username or password is incorrect')
   
   context = {'page': page}
   return render(request, 'login-register.html', context)


# ========== Logout View ========== #
def logoutUser(request):
   logout(request)
   return redirect('home')


# ========== Home View ========== #
def home(request):
   categories = requests.get('https://fakestoreapi.com/products/categories').json()
   
   context = {'categories':categories}
   return render(request, 'home.html', context)


# ========== ProductList View ========== #
def addProduct(request):
   id = request.POST.get('add')
   product = requests.get('https://fakestoreapi.com/products/{}'.format(id)).json()
   
   if Cart.objects.filter(cart_id = request.user.id).exists():
      cart = Cart.objects.get(cart_id = request.user.id)
      
      if Item.objects.filter(cart_id = request.user.id,product_id=product['id']).exists():
         item = Item.objects.get(cart_id = request.user.id, product_id = product['id'])
         item.quantity += 1
         item.save()
      else:
         new_item = Item.objects.create (
            cart_id = request.user.id,
            fav_id = 0,
            product_id = product['id'],
            name = product['title'],
            image = product['image'],
            price = product['price'],
            quantity = 1
         )
         new_item.save()
         cart.item.add(new_item)

   else:
      item = Item.objects.create(
         cart_id = request.user.id,
         fav_id = 0,
         product_id = product['id'],
         name = product['title'],
         image = product['image'],
         price = product['price'],
         quantity = 1
      )
      item.save()
      cart = Cart.objects.create(
         cart_id = request.user.id
      )
      cart.save()
      cart.item.add(item)


def addList(request):
   id = request.POST.get('add-list')
   list_name = request.POST.get('to-list')
   product = requests.get('https://fakestoreapi.com/products/{}'.format(id)).json()
   
   if FavList.objects.filter(favList_id = request.user.id, name=list_name).exists():
      fav_list = FavList.objects.get(favList_id = request.user.id, name=list_name)
      if Item.objects.filter(fav_id = request.user.id,product_id=product['id']).exists():
         return
      else:
         new_item = Item.objects.create (
            cart_id = 0,
            creator_id = request.user.id,
            fav_id = fav_list.id,
            product_id = product['id'],
            name = product['title'],
            image = product['image'],
            price = product['price'],
            quantity = 1
         )
         fav_list.item.add(new_item)

   else:
      fav_list = FavList.objects.create(
         favList_id = request.user.id,
         name=list_name
      )

      item = Item.objects.create(
         cart_id = 0,
         creator_id = request.user.id,
         fav_id = fav_list.id,
         product_id = product['id'],
         name = product['title'],
         image = product['image'],
         price = product['price'],
         quantity = 1
      )
      fav_list.item.add(item)


def productList(request, pk):
   productCategory = pk
   products = requests.get('https://fakestoreapi.com/products/category/{}'.format(productCategory)).json()
   favLists = FavList.objects.filter(favList_id = request.user.id)

   if 'add' in request.POST:
      addProduct(request)
   elif 'add-list' in request.POST:
      addList(request)

   context = {'productCategory': productCategory, 'products':products, 'favLists':favLists}
   return render(request, 'products.html', context)


# ========== Cart View ========== #
def cart(request):
   items = Item.objects.filter(cart_id = request.user.id)

   if Cart.objects.filter(cart_id = request.user.id).exists():
      cart = Cart.objects.get(cart_id=request.user.id)
   else:
      cart = Cart.objects.create(
            cart_id = request.user.id
         )

   if 'new-quantity' in request.POST:
      item_id = int(request.POST.get('item-to-inc') or 0)
      new_quantity = request.POST.get('new-quantity')
      if item_id != 0:
         item = Item.objects.get(product_id = item_id, cart_id = request.user.id)
         item.quantity = new_quantity
         item.save()

   elif 'remove' in request.POST:
      item_id = int(request.POST.get('remove') or 0)
      if item_id != 0:
         Item.objects.get(product_id=item_id, cart_id=request.user.id).delete()
         if not cart.item.all():
            cart.delete()
            cart = Cart.objects.create(
               cart_id = request.user.id
            )


   context = {'cart':cart}
   return render(request, 'cart.html', context)


# ========== Fav-Lists View ========== #
@login_required(login_url='login')
def favLists(request):
   lists = FavList.objects.filter(favList_id = request.user.id)

   
   if 'new-list' in request.POST:
      name = request.POST.get('new-list').lower()
      FavList.objects.create (
         favList_id = request.user.id,
         name = name
      )
   elif 'delete-list' in request.POST:
      list_id = int(request.POST.get('delete-list') or 0)
      if list_id != 0:
         FavList.objects.get(id=list_id).delete()
         Item.objects.filter(fav_id=list_id).delete()

   context = {'lists':lists}
   return render(request, 'favlist-menu.html', context)


@login_required(login_url='login')
# ========== Fav-List View ========== #
def favList(request,pk):
   items = Item.objects.filter(creator_id = request.user.id, fav_id = pk)
   list = FavList.objects.get(id=pk)

   if 'add' in request.POST:
      addProduct(request)

   elif 'remove' in request.POST:
      item_id = int(request.POST.get('remove') or 0)
      if item_id != 0:
         Item.objects.get(product_id=item_id, fav_id = pk).delete()

   context = {'items':items, 'list':list}
   return render(request, 'fav-list.html', context)


# ========== Profile View ========== #
def profile(request):
   context = {}
   return render(request, 'profile.html', context)


# ========== Checkout View ========== #
# def checkout_shipping(request):

#    if request.method == 'POST':
#       if Shipping.objects.filter(ship_id=request.user.id).exists():
#          new_data = {}
#          for field in request.POST:
#             if field == 'csrfmiddlewaretoken':
#                continue
#             else:
#                new_data[field] = request.POST.get(field)

#          Shipping.objects.filter(ship_id=request.user.id).update(**new_data)
#       else:
#          Shipping.objects.create (
#             ship_id = request.user.id,
#             name = request.POST.get('name'),
#             email = request.POST.get('email'),
#             address_1 = request.POST.get('address1'),
#             address_2 = request.POST.get('address2'),
#             zip_code = request.POST.get('zipCode'),
#             city = request.POST.get('city'),
#             country = request.POST.get('country')
#          )

#    context = {}
#    return render(request, 'checkout-shipping.html', context)


# ========== Order View ========== #
def order(request):
   customer = User.objects.get(id=request.user.id)
   order_name = str(customer.id)
   order_name += '_order'
   cart = Cart.objects.get(cart_id=customer.id)
   # shipping = Shipping.objects.get(ship_id=customer.id)
   products = cart.item.all()
   total = 0

   for product in products:
      total += product.price * product.quantity
   
   # if Order.objects.filter(customer = customer).exists():
   #    order = Order.objects.get(customer = customer)
   #    # order.shipping = shipping
   #    order.save()
   # else:
   #    order = Order.objects.create (
   #       name = order_name,
   #       customer = customer,
   #       cart = cart,
   #       amount = total,
   #       # shipping = shipping
   #    )

   context = {'cart':cart, 'amount':total}
   return render(request, 'order.html', context)


# ========== Order-Complete View ========== #
def orderComplete(request):
   data = json.loads(request.body)
   cart = Cart.objects.get(cart_id=request.user.id)
   # shipping = Shipping.objects.get(ship_id=customer.id)
   products = cart.item.all()
   total = 0

   for product in products:
      total += product.price * product.quantity

   received_total = float(data['amount'])
   date = datetime.now()
   dt_string = date.strftime("%d/%m/%Y %H:%M:%S")
   
   print(total, received_total)

   # if total == received_total:
   #    print('reach')
   customer = User.objects.get(id=request.user.id)
   order_name = 'order' + '_' + str(customer.id) + '_' + dt_string
   cart = Cart.objects.get(cart_id=customer.id)
   amount = total
   Order.objects.create (
      name = order_name,
      customer = customer,
      cart = cart,
      amount = amount,
      # shipping = shipping
   )



   return JsonResponse('Payment complete!', safe=False)
