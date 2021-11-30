from django.contrib import admin
from .models import MessDetails, User,Supplier,Customer,Feedback,MessReview,MessBooking


admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(MessDetails)
admin.site.register(Feedback)
admin.site.register(MessReview)
admin.site.register(MessBooking)



