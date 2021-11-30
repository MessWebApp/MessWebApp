from django.db import models
from django.contrib.auth.models import User , AbstractUser
from django.conf import settings
from datetime import date

from django.db.models import base
from django.http import request


class User(AbstractUser):
    number = models.CharField(max_length=12,null=True,blank=True)
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)



class Supplier(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=5000,null=True,blank=True)
    email = models.EmailField(max_length=3000)
    number = models.CharField(max_length=12,null=True,blank=True)
    image = models.ImageField(upload_to='supplierImage/', height_field=None, width_field=None, max_length=None)
    id_proof = models.ImageField(upload_to='supplier-id/', height_field=None, width_field=None, max_length=None)
    address = models.TextField(null=True,blank=True)
    acitve = models.BooleanField(default=False)
    date_of_joining = models.DateField(auto_now=False, auto_now_add=True)
    experience = models.IntegerField(default=0)
    otp = models.CharField(max_length=50,null=True,blank=True)
    email_verify = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=5000,null=True,blank=True)
    email = models.EmailField(max_length=3000)
    number = models.CharField(max_length=12,null=True,blank=True)
    image = models.ImageField(upload_to='customerImage/', height_field=None, width_field=None, max_length=None)
    id_proof = models.ImageField(upload_to='customer-id/', height_field=None, width_field=None, max_length=None)
    address = models.TextField(null=True,blank=True)
    acitve = models.BooleanField(default=False)
    date_of_joining = models.DateField(auto_now=False, auto_now_add=True)
    otp = models.CharField(max_length=50,null=True,blank=True)
    email_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.name

Type_CHOICES_Mess = (
    ('Veg', 'VEG'),
    ('Non-veg', 'NONVEG'),
)

class MessDetails(models.Model):
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    name = models.CharField(max_length=5000,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    map_link = models.URLField(max_length=10000,null=True,blank=True)
    rating = models.IntegerField(default=0)
    meal_type = models.CharField(max_length=200, choices=Type_CHOICES_Mess, default='', null=True, blank=True)
    meal_feature = models.TextField(null=True,blank=True)
    meal_special = models.TextField(null=True,blank=True)
    mess_availability = models.CharField(max_length=10000,null=True,blank=True)
    price_per_tiffin = models.IntegerField(default=0)
    price_per_month = models.IntegerField(default=0)
    mess_image1 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)
    mess_image2 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)
    mess_image3 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)
    mess_image4 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)


    def __str__(self):
        return self.name

class MessReview(models.Model):
    mess = models.ForeignKey(MessDetails, on_delete=models.CASCADE)
    content = models.CharField(max_length=50000,null=True,blank=True)

    def __str__(self):
        return str(self.mess)


class MessBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    mess = models.ForeignKey(MessDetails, on_delete=models.CASCADE)
    bookingId = models.IntegerField(default=0)
    booking_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.BooleanField(default=False)
    message = models.TextField(default="")
    
    def __str__(self):
        return self.bookingId
    


Type_CHOICES_rating = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(null=True, choices=Type_CHOICES_rating,default=0)
    content = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.content


class ContactMe(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=12)
    message = models.TextField(default="")

    def __str__(self):
        return self.name
    

    


    
    




    


