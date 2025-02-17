from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
   path('register/', views.registerPage, name='register'),
   path('logout/', views.logoutUser, name='logout'),
   path('profile/', views.profile, name='profile'),
   path('products/<str:pk>', views.productList, name='products'),
   path('cart/', views.cart, name='cart'),
   path('fav-lists/', views.favLists, name='fav-lists'),
   path('fav-list/<str:pk>', views.favList, name='fav-list'),
#    path('checkout-shipping', views.checkout_shipping, name='checkout-shipping'),
   path('order', views.order, name='order'),
   path('order-complete', views.orderComplete, name='order-complete'),
]
