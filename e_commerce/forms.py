from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User

# ========== User-Registration Form ========== #
class UserRegistration(UserCreationForm):
   class Meta:
      model = User
      fields = ['name', 'username', 'email', 'password1', 'password2']


# # ========== Shipping Form ========== #
# class ShippingForm(ModelForm):
#    class Meta:
#       model = Shipping
#       fields = '__all__'
#       exclude = ['ship_id']