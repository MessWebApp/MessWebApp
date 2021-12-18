from django.db import models
from django.contrib.auth.models import User , AbstractUser
from django.conf import settings
from datetime import date
from django.utils.text import slugify

from django.db.models import base
from django.http import request


class User(AbstractUser):
    number = models.CharField(max_length=12,null=True,blank=True)
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class State(models.Model):
    state = models.CharField(max_length=500)

    def __str__(self):
        return self.state

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.CharField(max_length=500)

    def __str__(self):
        return str(self.state) + "-" + str(self.district)


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.CharField( max_length=500)

    def __str__(self):
        return str(self.state)  + "-" + str(self.city)
    
    


class Supplier(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=5000,null=True,blank=True)
    email = models.EmailField(max_length=3000)
    number = models.CharField(max_length=12,null=True,blank=True)
    image = models.ImageField(upload_to='supplierImage/', height_field=None, width_field=None, max_length=None)
    id_proof = models.ImageField(upload_to='supplier-id/', height_field=None, width_field=None, max_length=None)
    address = models.TextField(null=True,blank=True)
    active = models.BooleanField(default=False)
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


class MessDetails(models.Model):
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    slug = models.SlugField(default="",blank=True,null=True)
    name = models.CharField(max_length=5000,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    number = models.CharField(max_length=12,blank=True,null=True)
    meal_type = models.CharField(max_length=200, null=True, blank=True)
    mess_availability = models.CharField(max_length=10000,null=True,blank=True)
    meal_feature = models.TextField(null=True,blank=True)
    meal_special = models.TextField(null=True,blank=True)
    map_link = models.URLField(max_length=10000,null=True,blank=True)
    rating = models.IntegerField(default=0)
    price_per_tiffin = models.IntegerField(default=0)
    price_per_month = models.IntegerField(default=0)
    price_with_veg = models.IntegerField(default=0)
    extra_for_non_veg = models.IntegerField(default=0)
    mess_image1 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)
    mess_image2 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)
    mess_image3 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)
    mess_image4 = models.ImageField(upload_to='messImage/', height_field=None, width_field=None,null=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name +"-"+ str(self.city))
        super(MessDetails, self).save(*args, **kwargs)

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
        return str(self.bookingId)
    
class RemindMe(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    mess = models.ForeignKey(MessDetails, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer)
    

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True,blank=True)
    rating = models.IntegerField(null=True,default=1)
    content = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.content)


class ContactMe(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=12)
    message = models.TextField(default="")

    def __str__(self):
        return self.name
    

    


    
    




    


