from rest_framework import generics,status, filters
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


# Create your views here.
## BUS ROUTES LOGICS
class BusRouteListCreateView(generics.ListCreateAPIView):
    queryset= BusRoute.objects.all()
    serializer_class = BusRouteSerializer


class BusRouteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer

class BusRouteSearchView(generics.ListAPIView):
    serializer_class = BusRouteSerializer
    permission_classes = [AllowAny]  # You can adjust permissions as needed
    filter_backends = [filters.SearchFilter]
    search_fields = ['route_name']  # Fields you want to search on

    def get_queryset(self):
        # Get the 'route_name' parameter from the query string
        search_query = self.request.GET.get('route_name', '')
        
        # Use the search query to filter the queryset
        queryset = BusRoute.objects.filter(route_name__icontains=search_query)
        
        return queryset


# bus logics

class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serialzer = self.get_serializer(data= request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response({'message': 'Bus created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]  # Restrict to admin users

    def retrieve(self, request, *args, **kwargs):
        bus_id = kwargs.get('pk')

        # Check if the bus exists, or return a 404 response
        bus = get_object_or_404(Bus, pk=bus_id)

        serializer = self.get_serializer(bus)
        return Response(serializer.data, status=status.HTTP_200_OK)

#stops 
class StopListCreateView(generics.ListCreateAPIView):
    queryset= Stop.objects.all()
    serializer_class= StopSerializer
    permission_classes = [AllowAny]

class StopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Stop.objects.all()
    serializer_class= StopSerializer
    permission_classes = [AllowAny]
    

##BOOKING LOGICS

#Booking creating 
class BookingCreateView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # later on we  can also handle payment and other booking-related steps.

        user = self.request.user

        # Get bus, route, and seat IDs from the request data
        bus_id= request.data.get('bus')
        route_id = request.data.get('route')
        seat_id = request.data.get('seats')

        # Check if the bus, route, and seats exist
        bus = get_object_or_404(Bus , bus_id)
        route = get_object_or_404(BusRoute, route_id)
        seats = Seat.objects.filter(pk__in =seat_id)

        # Check if the selected seats are available and do not exceed the bus's capacity
        unavailable_seats = seats.filter(status= 'reserved')
        if unavailable_seats or len(seats)> bus.capacity:
            return Response({'message': 'Selected seats are not available or exceed the bus capacity.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new booking
        booking = Booking(user=user, bus=bus, route=route)
        booking.save()
        booking.seats.set(seats)

         # Update seat statuses to 'reserved'
        seats.update(status = 'reserved')



        serializer= self.get_serializer(booking)

        response_data = {
            'message': 'Booking created successfully',
            'data':serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

# Retrieve Booking View# Retrieve Booking View
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        booking_id = kwargs.get('pk')

        # Check if the booking exists, or return a 404 response
        booking = get_object_or_404(Booking, pk=booking_id)

        # Check if the booking belongs to the current user (assuming you have user authentication)
        if booking.user != request.user:
            return Response({'message': 'This booking does not belong to you.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(booking)

        response = {
            "message": "Booking detail retrieved successfully",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)

# Booking Confirm View
class BookingConfirmView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def update(self, request, *args, **kwargs):
        booking_id = kwargs.get('pk')

        # Check if the booking exists, or return a 404 response
        booking = get_object_or_404(Booking, pk=booking_id)

        # Check if the booking belongs to the current user (assuming you have user authentication)
        if booking.user != request.user:
            return Response({'message': 'This booking does not belong to you.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the booking is already confirmed
        if booking.status == 'confirmed':
            return Response({'message': 'This booking is already confirmed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the booking as confirmed
        booking.status = 'confirmed'
        booking.save()

        # Mark the associated seats as 'reserved'
        booking.seats.update(status='reserved')

        serializer = self.get_serializer(booking)

        response = {
            "message": "Booking confirmed successfully",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)


# Booking History View
class BookingHistoryView(generics.ListAPIView):
    serializer_class = BookingHistorySerializer
    permission_classes= [IsAuthenticated]
    queryset= Booking.objects.all()

    def get_queryset(self):
        user = self.request.user  # Get the current user
        return Booking.objects.filter(user=user, status='confirmed').order_by('-created_at')

## seat logics 
class SeatListView(generics.ListAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class SeatDetailView(generics.RetrieveAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
  
#reservations
class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        bus_id  = request.data.get('bus')
        route_id  = request.data.get('route')
        seat_id = request.data.get('seats')

        bus = get_object_or_404(Bus , pk = bus_id)
        route  = get_object_or_404(BusRoute, pk = route_id)
        seat = Seat.objects.filter(pk__in= seat_id)

        #check if the seats are available
        unavailable_seats = seat.filter(status = 'reserved')
        if unavailable_seats:
            return Response({'message': 'Selected seats are not available.'}, status=status.HTTP_400_BAD_REQUEST)
        

        reservation = Reservation(user= user , bus = bus ,route = route, status ='pending', )
        reservation.save()
        reservation.seats.set(seat)

        seat.update(status = 'reserved')
        serializer = self.get_serializer(reservation)

        response_data = {
            'message': 'Reservation created successfully',
            'data': serializer.data
        }
        return Response(response_data , status=status.HTTP_201_CREATED)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]    

#payment
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user =self.request.user
        reservation_id =request.data.get('reservation')
        amount  = request.data.get('amount')

        reservation = get_object_or_404(Reservation, pk =reservation_id)

        payment = Payment(user = user ,reservation = reservation ,amount =amount)

        payment.save()
        serializer = self.get_serializer(payment)

        response_data = {
            'message': 'Payment created successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

