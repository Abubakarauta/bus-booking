from django.db import models
from users.models import Users  # Import the Users model

# Create your models here.

class Bus(models.Model):
    bus_number = models.CharField(max_length=100)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.bus_number
        
    

class Seat(models.Model):
    seat_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[("available", "Available"), ("reserved", "Reserved")])
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return self.seat_number
    


class Stop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        


class BusRoute(models.Model):
    route_name = models.CharField(max_length=200)
    stops = models.ManyToManyField(Stop)
    estimated_travle_time = models.TimeField()


    def __str__(self):
        return self.route_name

    
    


class Reservation(models.Model):
    reservation_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)  # Each reservation is associated with a bus
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed")])
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Reservation by {self.user.email} on {self.reservation_date}"
    


class Payment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment by {self.user.email} on {self.payment_date}"
    
class Booking(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.email} for {self.bus.bus_number}"