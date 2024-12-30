from django import forms
from .models import ClothingItem,AdditionalImage,Order, Status
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = '__all__'

class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'quantity', 'contact_number']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    address = forms.CharField(max_length=500, help_text='Enter your address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'address', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


