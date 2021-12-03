from django.urls import path

from . import views

urlpatterns = [
    path('',views.Home,name='Home'),
    path('contact-us/',views.ContactUs,name='contact'),

    #  ================== customer login ==================
    path('customer-login/',views.CustomerLoginView,name='customer-login'),
    path('customer-sendOtp/',views.CustomerSendOPT,name='customer-otp'),
    path('customer-register/',views.CustomerRegister,name='customer-register'),
    path('customer-userpanal/',views.CustomerUserPanal,name='customer-userpanal'),

    #  ================== customer login ==================
    path('supplier-login/',views.SupplierLoginView,name='supplier-login'),
    path('supplier-register/',views.SupplierRegister,name='supplier-register'),
]