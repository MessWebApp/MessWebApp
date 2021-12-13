from django.contrib import admin

from .models import MessDetails, User,Supplier,Customer,Feedback,MessReview,MessBooking,ContactMe,State , District , City,RemindMe


admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(MessDetails)
admin.site.register(Feedback)
admin.site.register(MessReview)
admin.site.register(MessBooking)
admin.site.register(ContactMe)
admin.site.register(RemindMe)
admin.site.register(State)
admin.site.register(District)
admin.site.register(City)



