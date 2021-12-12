from django.urls import path

from . import views

urlpatterns = [
    path('',views.Home,name='Home'),
    path('contact-us/',views.ContactUs,name='contact'),
    path('logout/',views.LogoutView,name='logout'),

    #  ================== customer login ==================
    path('customer-login/',views.CustomerLoginView,name='customer-login'),
    path('customer-sendOtp/',views.CustomerSendOPT,name='customer-otp'),
    path('customer-register/',views.CustomerRegister,name='customer-register'),
    path('customer-userpanal/',views.CustomerUserPanal,name='customer-userpanal'),
    path('customer-details/<str:pk>',views.CustomerDetails,name='customer-details'),

    #  ================== customer login ==================
    path('supplier-login/',views.SupplierLoginView,name='supplier-login'),
    path('supplier-register/',views.SupplierRegister,name='supplier-register'),
    path('supplier-userpanal/',views.SupplierUserpanal,name='supplier-userpanal'),
    path('add-supplier-mess/',views.AddMessDetails,name='add-supplier-mess'),
    path('supplier-sendOtp/',views.SupplierSendOPT,name='supplier-otp'),
    path('supplier-details/<str:pk>',views.SupplierUserDetails,name='supplier-details'),
]