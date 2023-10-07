from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Bus)
admin.site.register(BusRoute)
admin.site.register(Booking)
admin.site.register(Reservation)
admin.site.register(Seat)
admin.site.register(Payment)

