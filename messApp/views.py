from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages 
from django.conf import settings

# from django.contrib.auth.models import User
from .models import City, Customer, District, Feedback, State,Supplier,MessDetails,MessBooking,MessReview,User
import random
from django.core.mail import EmailMessage, message , send_mail
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
    all_mess = MessDetails.objects.all()
    all_user = len(User.objects.filter(is_superuser = False))
    all_customer = len(Customer.objects.all())
    all_supplier = len(Supplier.objects.all())
    feedbacks = Feedback.objects.all()

    states = State.objects.all()
    districts = District.objects.all()
    cities = City.objects.all()
    
    context = {
        'customer':customer,
        'supplier':supplier,
        'all_mess':all_mess,
        'all_user':all_user,
        'all_customer':all_customer,
        'all_supplier':all_supplier,
        'feedbacks':feedbacks,
        'states':states,
        'districts':districts,
        'cities':cities
    }
    return render(request,'index.html',context)

def SearchWithCity(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    city = request.GET.get('city')
    customer =None
    supplier =None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = user)
        elif Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)

    all_mess = MessDetails.objects.filter(state = state,city = city)

    context ={
        'customer':customer,
        'supplier':supplier,
        'state':state,
        'district':district,
        'city':city,
        'all_mess':all_mess,
    }
    return render(request,'searchResult.html',context)

def SearchWithInput(request):
    search = request.GET.get('search')
    customer =None
    supplier =None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = user)
        elif Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)

    all_mess = MessDetails.objects.filter(name__icontains =search)

    context ={
        'search':search,
        'customer':customer,
        'supplier':supplier,
        'all_mess':all_mess,
    }
    return render(request,'searchResult.html',context)

def AllSupplier(request):
    customer =None
    supplier =None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = user)
        elif Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
    all_mess = MessDetails.objects.all()

    context = {
        'all_mess':all_mess,
        'customer':customer,
        'supplier':supplier
    }

    return render(request,'all-suppliers.html',context)




def SupplierList(request):
    suppliers = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if user is not None:
            if user.is_superuser:
                suppliers = Supplier.objects.all()
                count_sup = len(suppliers)
                len_active = len(Supplier.objects.filter(active = True))
                count_not_act = len(Supplier.objects.filter(active = False))
                context = {
                    'suppliers':suppliers,
                    'active_count':len_active,
                    'total_count':count_sup,
                    'not_active':count_not_act
                }
                return render(request,'list-of-suppliers.html',context)

    return redirect('/')


def AdminAction(request):
    suppliers = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if user is not None:
            if user.is_superuser:
                if request.method == 'POST':
                    label = request.POST.get('label')
                    supplier_id = request.POST.get('supplier_id')
                
                    supplier = Supplier.objects.get(id = supplier_id)
                    supplier.label = label
                    if label == 'accept':
                        supplier.active = True
                        messages.success(request,'Your Account is activated.')
                    elif label == 'declined':
                        messages.warning(request,'Your Account is Not activated.')

                    supplier.save()
                    return redirect('/supplier-list')
    return redirect('/')




def EachMess(request,slug):
    customer =None
    supplier =None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = user)
        elif Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
    print(supplier)
    mess = MessDetails.objects.get(slug = slug)
    context = {
        'mess':mess,
        'supplier':supplier,
        'customer':customer
    }

    return render(request,'product-details.html',context)


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
            return render(request,'supplier/supplier-register.html',{'name':name,'email':email,'number':number})

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
                messages.success(request,'Your account is activated. Enjoy the experience of our site')
                return redirect('/supplier-login')
            else:
                messages.info(request,'otp is wrong please try again')
                return redirect('/supplier-sendOTP')
        
        return render(request,'supplier/supplier-otp.html',{'email':email})
    else:
        return redirect('/supplier-login')

def RecentOPT(request):
    email = request.session['email']
    if email:
        supplier = Supplier.objects.get(email = email)

        mail_body = f'Hello {supplier.name}, \n welcome to messo web App. \n for verification her is your otp {supplier.otp}.\n enjoy the journey.'

        mail = EmailMessage(
            subject='Account Verification',
            body=mail_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[email,]
            )
        mail.send()

        messages.success(request,'OTP is recent to your Mail.')
        return render(request,'supplier/supplier-otp.html',{'email':email})


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

            if mess_details is None:
                return redirect('/add-supplier-mess')
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


def EditMessDetails(request):
    if request.user.is_active:
        supplier = None
        mess = None
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
            if MessDetails.objects.filter(supplier = supplier).exists():
                mess = MessDetails.objects.get(supplier = supplier)
            
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
                    

                    mess.name = name
                    mess.state = state
                    mess.city = city
                    mess.address = address
                    mess.number = number
                    mess.meal_type = meal_type
                    mess.mess_availability = mess_availability
                    mess.meal_feature = mess_feature
                    mess.meal_special = mess_special
                    mess.map_link = mess_map_link
                    mess.rating = rating
                    mess.price_per_tiffin = price_per_tiffin
                    mess.price_per_month = price_per_month
                    mess.price_with_veg = price_with_veg
                    mess.extra_for_non_veg = extra_for_non_veg

                    if image1 is not None:
                        mess.mess_image1 = image1
                    if image2 is not None:
                        mess.mess_image2 = image2
                    if image3 is not None:
                        mess.mess_image3 = image3
                    if image4 is not None:
                        mess.mess_image4 = image4
                    
                    mess.save()
                    messages.success(request,'Mess Details Successfully Updated.')
            return render(request,'supplier/edit-messDetails.html',{'mess':mess,'supplier':supplier})

        return redirect('/supplier-login')
    
    return redirect('/supplier-login')


def SupplierCustomersRequest(request):
    if request.user.is_active:
        supplier = None
        mess = None
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
            mess = MessDetails.objects.get(supplier = supplier)
            bookings = MessBooking.objects.filter(mess = mess)
            if len(bookings) == 0:
                return redirect('/supplier-userpanal')

            context = {
                'bookings':bookings,
                'supplier':supplier,
                'mess':mess
            }

            return render(request,'supplier/customer-request.html',context)

        return redirect('/supplier-login')
    
    return redirect('/supplier-login')


def SupplierAcceptBooking(request):
    if request.user.is_active:
        supplier = None
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
            if request.method == 'POST':
                bookingId = request.POST.get('bookingId')
                value = request.POST.get('value')
                message = request.POST.get('message')

                bookingMess = MessBooking.objects.get(bookingId = bookingId)
                if value == 'accept':
                    bookingMess.status = True
                    bookingMess.label = 'accept'
                elif value == 'reject':
                    bookingMess.label = 'reject'
                bookingMess.message = message
                bookingMess.save()
                customer = Customer.objects.get(id = bookingMess.customer.id)
                mail_body = f'Hello {customer.name}, \n welcome to messo web App. \n Your Request is accepted by the supplier. \n your mess continue from tonight not your given address. \n regards, \n {supplier.name} \n {supplier.number}'

                mail = EmailMessage(
                    subject='Accept Mess Request',
                    body=mail_body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[customer.email,]
                    )
                mail.send()

                messages.success(request,'Booking Is Approved.')
                return redirect('/supplier-requests')

        return redirect('/supplier-login')
    
    return redirect('/supplier-login')


def SupplierCustomers(request):
    if request.user.is_active:
        supplier = None
        mess = None
        user = User.objects.get(username = request.user.username)
        if Supplier.objects.filter(user = user).exists():
            supplier = Supplier.objects.get(user = user)
            mess = MessDetails.objects.get(supplier = supplier)
            bookings = MessBooking.objects.filter(mess = mess,status = True)
            if len(bookings) == 0:
                return redirect('/supplier-userpanal')

            context = {
                'bookings':bookings,
                'supplier':supplier,
                'mess':mess
            }
            return render(request,'supplier/supplier-customer.html',context)

        return redirect('/supplier-login')
    
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
                    return redirect('/customer-userpanal')
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
                messages.success(request,'Your account is activated. Enjoy the experience of our site')
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
            booking = MessBooking.objects.filter(customer = customer)
            if len(booking) == 0:
                return redirect('/customer-editProfile')

            if not customer.address or not customer.id_proof:
                return redirect('/customer-editProfile')

        context = {
            'customer':customer,
            'bookings':booking
        }
    else:
        return redirect('/customer-login')

    return render(request,'customer/customer-userpanal.html',context)

def BookMess(request,slug):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            mess = MessDetails.objects.get(slug = slug)
            supplier = Supplier.objects.get(id = mess.supplier.id)

            booking_id = random.randint(100000,9999999)
            if MessBooking.objects.filter(bookingId = booking_id).exists():
                booking_id = random.randint(100000,9999999)
            
            if MessBooking.objects.filter(customer = customer , mess = mess).exists():
                messages.info(request,'you Have Already Booked The Mess')
                return redirect('/customer-userpanal')

            booking = MessBooking(customer = customer,mess = mess,bookingId = booking_id ,message = 'Book the mess')
            booking.save()
            messages.success(request,'You Have Successfully Booked the Mess. \n wait for Approval.')
            mail_body = f'Hello {supplier.name}, \n welcome to messo web App. \n Our Customer {customer.name} having Mail {customer.email} \n number : {customer.number} \n Address : {customer.address} \n Check your dashboard and perform specific action.'

            mail = EmailMessage(
                    subject='Accept Mess Request',
                    body=mail_body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[supplier.email,]
                    )
            mail.send()
            return redirect('/customer-userpanal')
    else:
        return redirect('/customer-login')
    return redirect('/customer-login')

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


def CustomerHistory(request):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            booking = MessBooking.objects.filter(customer = customer)
            if len(booking) == 0:
                return redirect('/customer-userpanal')
            context = {
                'customer':customer,
                'bookings':booking
            }
            return render(request,'customer/customer-history.html',context)
    else:
        return redirect('/customer-login')
    
    return redirect('/customer-login')

def CustomerEditProfile(request):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                name = request.POST.get('name')
                number = request.POST.get('number')
                address = request.POST.get('address')
                addhar = request.FILES.get('id_proof')

                customer.name = name
                customer.number = number
                if addhar:
                    customer.id_proof = addhar
                customer.address = address
                customer.save()
                messages.success(request,'profile Info Successfully Updated')
                return redirect('/customer-editProfile')

            context = {
                'customer':customer
            }

            return render(request,'customer/customer-edit.html',context)
    else:
        return redirect('/customer-login')
    
    return redirect('/customer-login')

def CustomerEditProfilePic(request):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            print('hello world')
            if request.method == 'POST':
                profile = request.FILES.get('profile')
                customer.image = profile
                customer.save()
                messages.success(request,'profile Pic Successfully Updated')
                return redirect('/customer-editProfile')

            context = {
                'customer':customer
            }

            return render(request,'customer/customer-edit.html',context)
    else:
        return redirect('/customer-login')
    
    return redirect('/customer-login')



def CustomerFeedback(request):
    customer = None
    if request.user.is_active:
        user = User.objects.get(username = request.user.username)
        if Customer.objects.filter(user = user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                rating = request.POST.get('rating')
                content = request.POST.get('content')

                feedback = Feedback(customer = customer , rating = rating,content = content)
                feedback.save()

                messages.success(request,'Your Feedback is Received.')
                return redirect('/customer-userpanal')
            context = {
                'customer':customer
            }

            return render(request,'customer/customer-feedback.html',context)
    else:
        return redirect('/customer-login')
    
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




