from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages 
from django.conf import settings

# from django.contrib.auth.models import User
from .models import Customer,Supplier,MessDetails,MessBooking,MessReview,User
import random
from django.core.mail import EmailMessage , send_mail
from .form import ContactForm

# Create your views here.
def Home(request):
    print(request.user)
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
        from_email=settings.EMAIL_HOST_USER,
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

#===================== supplier userpanal =========================

def SupplierUserpanal(request):
    return render(request,'supplier-userpanal.html',{})



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
                    print('hello world')
                    redirect('/customer-userpanal')
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

        mail_body = f'Hello {name}, \n welcome to messo web App. \n for verification her is your otp {otp}.\n enjoy the journey.'


        mail = EmailMessage(
        subject='Account Verification',
        body=mail_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[email,]
        )
        mail.send()
        messages.success(request,'Verfiy your Profile.Otp sended to your email.')
        return redirect('/customer-sendOtp')

    return render(request,'customer/customer-register.html',{})


def CustomerSendOPT(request):
    email = request.session['email']
    if len(email) != 0:
        customer = Customer.objects.get(email = email)

        if request.method == 'POST':
            otp = request.POST.get('otp')

            if customer.otp == otp:
                request.session['email'] = ''
                customer.email_verify = True
                customer.save()
                messages.info(request,'Your account is activated. Enjoy the experience of our site')
                return redirect('/customer-login')
            else:
                messages.info(request,'otp is wrong please try again')
    else:
        return redirect('/customer-login')
    
    return render(request,'customer/customer-otp.html',{'email':email})



def CustomerUserPanal(request):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            if customer.address == 0 or not customer.id_proof:
                return redirect('/')

        context = {
            'customer':customer
        }
    else:
        return redirect('/customer-login')

    return render(request,'customer/customer-userpanal.html',context)




# =========================== contact page ====================

def ContactUs(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            form.save_m2m()
            messages.success(request,'Your Response is accepted. We Contact You Sortly')
            return redirect('/')

    context = {
        'form':form
    }
    return render(request,'contactus.html',context)




