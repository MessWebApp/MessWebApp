from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
# from django.contrib.auth.models import User
from .models import Customer,Supplier,MessDetails,MessBooking,MessReview,User
import random
from django.core.mail import EmailMessage , send_mail

# Create your views here.
def Home(request):
    return render(request,'index.html',{})

def Search(request):
    return render(request,'serach.html',{})


#  ======================== supplier login ===========================
def SupplierLoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = email,password = password)

        if user is not None:
            if user.is_active and user.is_supplier:
                supplier = Supplier.objects.get(user = user)
                if supplier.email_verify:
                    login(request,user)
                    redirect('')
                else:
                    messages.warning(request,'your account not verified please verified then login.')
                    redirect('/email-verification')
        else:
            messages.warning(request,'Please check the credential')
            return redirect('/supplier-login')

    context = {}
    return render(request,'supplier/supplier-login.html',context)

# =================== register supplier =============================

def SupplierRegister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        vpassword = request.POST.get('vpassword')
        password = request.POST.get('password')

        if User.objects.filter(email = email,number=number).exists():
            messages.warning(request,'user is Exits please login in site.')
            return redirect('/supplier-login')
        
        if password != vpassword:
            messages.warning(request,'Password is not veririfed check again.')
            return redirect('/supplier-login')

        user = User(email = email,first_name = name,number = number,username = email,is_supplier = True)
        user.set_password(password)
        user.save()

        otp = str(random.randint(10000,99999))
        if Supplier.objects.filter(otp = otp).exists():
            otp = str(random.randint(10000,99999))

        request.session['email'] = email

        supplier = Supplier(name = name,email = email,number = number,otp = otp)
        supplier.save()

        mail = EmailMessage(
        subject='hellow rodld',
        body='email Body',
        from_email='settings.EMAIL_HOST_USER',
        to=[email,]
        )
        mail.send()
        messages.success(request,'Verfiy your Profile.Otp sended to your email.')
        return redirect('/supplier-sendOTP')

    return render(request,'supplier/supplier-register.html',{})


def SupplierSendOPT(request):
    email = request.session['email']
    supplier = Supplier.objects.get(email = email)

    if request.method == 'POST':
        otp = request.POST.get('otp')

        if supplier.otp == otp:
            request.session['email'] = ''
            supplier.email_verify = True
            supplier.save()
        else:
            messages.info(request,'otp is wrong please try again')
            return redirect('/supplier-sendOTP')
    
    return render(request,'supplier-otp.html',{'email':email})


# =================== register supplier =============================



# ======================== customer login =========================
def CustomerLoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = email,password = password)

        if user is not None:
            if user.is_active and user.is_customer:
                customer = Customer.objects.get(user = user)
                if customer.email_verify:
                    login(request,user)
                    redirect('')
                else:
                    messages.warning(request,'your account not verified please verified then login.')
                    redirect('/email-verification')
        else:
            messages.warning(request,'Please check the credential')
            return redirect('/customer-login')

    context = {}
    return render(request,'customer/customer-login.html',context)


def CustomerRegister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        vpassword = request.POST.get('vpassword')
        password = request.POST.get('password')

        if User.objects.filter(username = email,number=number).exists():
            messages.warning(request,'user is Exits please login in site.')
            return redirect('/customer-login')
        
        if password != vpassword:
            messages.warning(request,'Password is not veririfed check again.')
            return redirect('/customer-login')

        user = User(email = email,first_name = name,number = number,username = email,is_customer = True)
        user.set_password(password)
        user.save()

        otp = str(random.randint(10000,99999))
        if Customer.objects.filter(otp = otp).exists():
            otp = str(random.randint(10000,99999))

        request.session['email'] = email

        customer = Customer(user = user, name = name,email = email,number = number,otp = otp)
        customer.save()

        mail = EmailMessage(
        subject='hellow rodld',
        body='email Body',
        from_email='settings.EMAIL_HOST_USER',
        to=[email,]
        )
        mail.send()
        messages.success(request,'Verfiy your Profile.Otp sended to your email.')
        return redirect('/customer-sendOTP')

    return render(request,'customer/customer-register.html',{})


def CustomerSendOPT(request):
    email = request.session['email']
    customer = Customer.objects.get(email = email)

    if request.method == 'POST':
        otp = request.POST.get('otp')

        if customer.otp == otp:
            request.session['email'] = ''
            customer.email_verify = True
            customer.save()
        else:
            messages.info(request,'otp is wrong please try again')
            return redirect('/customer-sendOTP')
    
    return render(request,'customer-otp.html',{'email':email})



#===================== supplier userpanal =========================

def SupplierUserpanal(request):
    return render(request,'supplier-userpanal.html',{})


