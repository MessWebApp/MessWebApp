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
    customer =None
    supplier =None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = user)
        elif Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
    
    context = {
        'customer':customer,
        'supplier':supplier
    }
    return render(request,'index.html',context)

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
                    return redirect('/supplier-userpanal')
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

        supplier = Supplier(user = user,name = name,email = email,number = number,otp = otp)
        supplier.save()

        mail_body = f'Hello {name}, \n welcome to messo web App. \n for verification her is your otp {otp}.\n enjoy the journey.'


        mail = EmailMessage(
        subject='Account Verification',
        body=mail_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[email,]
        )
        mail.send()

        messages.success(request,'Verfiy your Profile.Otp sended to your email.')
        return redirect('/supplier-sendOtp')

    return render(request,'supplier/supplier-register.html',{})


def SupplierSendOPT(request):
    email = request.session['email']
    if email:
        supplier = Supplier.objects.get(email = email)

        if request.method == 'POST':
            otp = request.POST.get('otp')

            if supplier.otp == otp:
                request.session['email'] = ''
                supplier.email_verify = True
                supplier.save()
                return redirect('/supplier-userpanal')
            else:
                messages.info(request,'otp is wrong please try again')
                return redirect('/supplier-sendOTP')
        
        return render(request,'supplier/supplier-otp.html',{'email':email})
    else:
        return redirect('/supplier-login')


# =================== register supplier =============================

#===================== supplier userpanal =========================

def SupplierUserpanal(request):
    if request.user.is_active:
        supplier = None
        mess_details = None
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
            mess_details = MessDetails.objects.filter(supplier = supplier).first()
            if not supplier.address or not supplier.id_proof:
                messages.info(request,'complete Your Profile.')
                return redirect(f'/supplier-details/{supplier.id}')
        context = {
            'supplier':supplier,
            'mess':mess_details
        }
            
        return render(request,'supplier/supplier-userpanal.html',context)

    return redirect('/supplier-login')

def SupplierUserDetails(request,pk):
    supplier = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = request.user)
            if request.method == 'POST':
                address = request.POST.get('address')
                id_proof = request.FILES.get('id_proof')

                supplier.address = address
                supplier.id_proof = id_proof
                supplier.save()
                messages.success(request,'Your details is updated Enjoy the Journey.')
                return redirect('/supplier-userpanal')
        
        else:
            return redirect('/supplier-login')
        
        return render(request,'supplier/fill-details.html',{'supplier':supplier})

    return redirect('/supplier-login')


def AddMessDetails(request):
    if request.user.is_active:
        supplier = None
        mess_details = None
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
            if request.method == 'POST':
                name = request.POST.get('mess_name')
                state = request.POST.get('state')
                city = request.POST.get('city')
                address = request.POST.get('address')
                number = request.POST.get('number')
                meal_type = request.POST.get('meal_type')
                mess_availability = request.POST.get('mess_availability')
                mess_feature = request.POST.get('meal_feature')
                mess_special = request.POST.get('meal_special')
                mess_map_link = request.POST.get('map_link')
                rating = request.POST.get('rating')
                price_per_tiffin = request.POST.get('per_tiffin')
                price_per_month = request.POST.get('per_week')
                price_with_veg = request.POST.get('price_with_veg')
                extra_for_non_veg = request.POST.get('extra_for_non_veg')
                image1 = request.FILES.get('image1')
                image2 = request.FILES.get('image2')
                image3 = request.FILES.get('image3')
                image4 = request.FILES.get('image4')
            
                addMess = MessDetails(supplier = supplier , name = name,state = state,city = city , address = address , 
                number = number,meal_type = meal_type,mess_availability = mess_availability , meal_feature = mess_feature , 
                meal_special = mess_special , map_link = mess_map_link,rating = rating , price_per_tiffin = price_per_tiffin,
                price_with_veg = price_with_veg , extra_for_non_veg = extra_for_non_veg, 
                price_per_month = price_per_month , mess_image1 = image1 , mess_image2 = image2 , mess_image3 = image3 , mess_image4 = image4)

                addMess.save()

                messages.success(request,'Mess Details is Added!')
                return redirect('/supplier-userpanal')

        context = {
            'supplier':supplier,
        }
        return render(request,'supplier/supplier-mess.html',context)

    return redirect('/supplier-login')
    



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
            if not customer.address or not customer.id_proof:
                return redirect(f'/customer-details/{customer.id}')

        context = {
            'customer':customer
        }
    else:
        return redirect('/customer-login')

    return render(request,'customer/customer-userpanal.html',context)

def CustomerDetails(request,pk):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                address = request.POST.get('address')
                id_proof = request.FILES.get('id_proof')

                print(id_proof)

                customer.address = address
                customer.id_proof = id_proof
                customer.save()
                messages.success(request,'Your details is updated Enjoy the Journey.')
                return redirect('/customer-userpanal')
        
        else:
            return redirect('/customer-login')
        
        return render(request,'customer/fill-details.html',{'customer':customer})

    return redirect('/customer-login')




# ================================ logout section ==============================

def LogoutView(request):
    if request.user.is_active:
        logout(request)
        messages.success(request,'You SuccessFully Logout.')
    
    return redirect('/')

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




