from django.shortcuts import render
from .models import ClothingItem
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClothingItemForm, AdditionalImageForm, OrderForm
from .models import ClothingItem, Order, UserProfile, Status
from django.contrib.auth import login, authenticate
from .forms import SignUpForm,LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
import time
import pywhatkit 
import pyautogui
import keyboard as k
from django.templatetags.static import static
from django.conf import settings

@login_required(login_url='login_view')
def index(request):
    clothes = {'index': ClothingItem.objects.all().order_by('-id')}
    return render(request, 'cloth_register/index.html', clothes)

@login_required(login_url='login_view')
def product_detail(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id)
    return render(request, 'cloth_register/product_detail.html', {'item': item})

@user_passes_test(lambda u: u.is_superuser)
def create_clothing_item(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ClothingItemForm()
    return render(request, 'cloth_register/create_clothing_item.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def upload_additional_images(request, item_id):
    item = get_object_or_404(ClothingItem, pk=item_id)
    if request.method == 'POST':
        form = AdditionalImageForm(request.POST, request.FILES)
        if form.is_valid():
            additional_image = form.save(commit=False)
            additional_image.clothing_item = item
            additional_image.save()
            return redirect('upload_additional_images', item_id=item_id)
    else:
        form = AdditionalImageForm()
    return render(request, 'cloth_register/upload_additional_images.html', {'form': form, 'item': item})

@login_required(login_url='login_view')
def place_order(request,item_id):
    item = get_object_or_404(ClothingItem, pk=item_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.clothing_item = item
            form.save()
            ordered_status,created= Status.objects.get_or_create(order_status='Ordered')
            order.status = ordered_status
            order.save()
            return render(request, 'cloth_register/order_confirmation.html', {'item': item})
    else:
        form = OrderForm()
    return render(request, 'cloth_register/order.html', {'form': form, 'item': item})

@user_passes_test(lambda u: u.is_superuser)
def display_orders(request):
    orders = Order.objects.select_related('clothing_item').all()
    statuses = Status.STATUS_CHOICES
    return render(request, 'cloth_register/display_orders.html', {'orders': orders, 'statuses': statuses})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            is_admin = request.POST.get('is_admin', False)
            user_profile = UserProfile.objects.create(user=user, address=form.cleaned_data['address'], is_admin=is_admin)
            return redirect('login_view')
    else:
        form = SignUpForm()
    return render(request, 'cloth_register/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'cloth_register/login.html', {'form': form})

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order_status_value = request.POST.get('order_status')
        if order_status_value is not None:
            try:
                status = Status.objects.get(order_status=order_status_value)
                order.status = status
                order.save()
                contact = "1" + str(order.contact_number)
                print(contact)
                details = f"Hello {order.name},\n\nWe wanted to update you on your order:\n\nCustomer: {order.name}\nAddress: {order.address}\nQuantity: {order.quantity}\nStatus: {order.status.order_status}\n\nThank you for choosing our services!"
                print(details)
                try:
                    time.sleep(2)
                    pywhatkit.sendwhatmsg_instantly(f"+{contact}", details)
                    pyautogui.click(1050, 950)
                    k.press('enter')
                    pyautogui.hotkey('ctrl', 'i')
                    pyautogui.press('enter')
                    message = f"Order details sent via WhatsApp to {contact} instantly."
                    
                except Exception as e:
                    message = f"Error: {e}"
                    print(message)
            except Status.DoesNotExist:
                print(f"Status matching query does not exist for value: {order_status_value}")

    return redirect('display_orders')