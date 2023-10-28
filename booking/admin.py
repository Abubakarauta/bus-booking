from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(BusRoute)
admin.site.register(Booking)
admin.site.register(Reservation)
admin.site.register(Seat)
admin.site.register(Payment)
admin.site.register(Stop)

class SeatInline(admin.StackedInline):
    extra = 1
    model = Seat



# admin.site.register(Bus)
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    inlines = [SeatInline]