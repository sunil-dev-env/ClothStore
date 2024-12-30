from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name='login_view'),
    path('index/', views.index, name='index'),
    path('create/', views.create_clothing_item, name='create_clothing_item'),
    path('upload/<int:item_id>/', views.upload_additional_images, name='upload_additional_images'),
    path('details/', views.product_detail, name='product_detail'),
    path('<int:item_id>/', views.product_detail, name='product_detail'),
    path('order/<int:item_id>/', views.place_order, name='place_order'),
    path('display_orders/', views.display_orders, name='display_orders'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),


    # Add other URLs as needed

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
