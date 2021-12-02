from django.urls import path

from . import views

urlpatterns = [
    path('',views.Home,name='Home'),

    #  ================== customer login ==================
    path('customer-login/',views.CustomerLoginView,name='customer-login'),
    path('customer-register/',views.CustomerRegister,name='customer-register'),

    #  ================== customer login ==================
    path('supplier-login/',views.SupplierLoginView,name='supplier-login'),
    path('supplier-register/',views.SupplierRegister,name='supplier-register'),
]