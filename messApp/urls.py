from django.urls import path

from . import views

urlpatterns = [
    path('',views.Home,name='Home'),
    path('contact-us/',views.ContactUs,name='contact'),
    path('all-supplier/',views.AllSupplier,name='all-supliers'),
    path('mess/<slug>',views.EachMess,name='mess'),
    path('logout/',views.LogoutView,name='logout'),
    path('bookMess/<slug>',views.BookMess,name='book-mess'),
    path('search-with-city/',views.SearchWithCity,name='search-with-city'),
    path('search/',views.SearchWithInput,name='search-with-input'),

    #  ================== customer login ==================
    path('customer-login/',views.CustomerLoginView,name='customer-login'),
    path('customer-sendOtp/',views.CustomerSendOPT,name='customer-otp'),
    path('customer-register/',views.CustomerRegister,name='customer-register'),
    path('customer-userpanal/',views.CustomerUserPanal,name='customer-userpanal'),
    path('customer-details/<str:pk>',views.CustomerDetails,name='customer-details'),
    path('customer-history/',views.CustomerHistory,name='customer-history'),
    path('customer-editProfile/',views.CustomerEditProfile,name='customer-profile'),
    path('customer-editProfilePic/',views.CustomerEditProfilePic,name='customer-profile-pic'),
    path('customer-feedback/',views.CustomerFeedback,name='customer-feedback'),

    #  ================== customer login ==================
    path('supplier-login/',views.SupplierLoginView,name='supplier-login'),
    path('supplier-register/',views.SupplierRegister,name='supplier-register'),
    path('supplier-userpanal/',views.SupplierUserpanal,name='supplier-userpanal'),
    path('add-supplier-mess/',views.AddMessDetails,name='add-supplier-mess'),
    path('edit-supplier-mess/',views.EditMessDetails,name='edit-supplier-mess'),
    path('supplier-sendOtp/',views.SupplierSendOPT,name='supplier-otp'),
    path('supplier-details/<str:pk>',views.SupplierUserDetails,name='supplier-details'),
    path('supplier-requests/',views.SupplierCustomersRequest,name='supplier-request'),
    path('supplier-request-accept/',views.SupplierAcceptBooking,name='supplier-request-accept'),
    path('supplier-customers/',views.SupplierCustomers,name='supplier-customers'),

    #  ================== Super user system ==================
    path('supplier-list/',views.SupplierList,name='supplier-list'),
    path('supplier-action/',views.AdminAction,name='supplier-action'),
    path('recant-otp/',views.RecentOPT,name='recant-otp'),




]