from rest_framework import generics,status, filters
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
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
    permission_classes = [IsAdminUser]


class BusRouteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes =[IsAdminUser]

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




# class BusSearchView(generics.ListAPIView):
#     serializer_class = BusSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         # Access query parameters using the get() method
#         departure_location = self.request.GET.get('departure_location')
#         arrival_location = self.request.GET.get('arrival_location')

#         # Use the query parameters to filter the queryset
#         queryset = Bus.objects.filter(
#             departure_location__iexact=departure_location,
#             arrival_location__iexact=arrival_location
#         )

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = BusSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


#stops 
class StopListCreateView(generics.ListCreateAPIView):
    queryset= Stop.objects.all()
    serializer_class= StopSerializer
    permission_classes = [IsAdminUser]

class StopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Stop.objects.all()
    serializer_class= StopSerializer
    permission_classes = [IsAdminUser]
    

##BOOKING LOGICS

#Booking creating 
class BookingCreateView(generics.ListCreateAPIView):
    queryset= Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        print(user)
        bus_pk = request.data.get('bus')
        route = request.data.get('route')
        seat_id = request.data.get('seats')

        print(bus_pk, route,seat_id)
        bus = get_object_or_404(Bus, pk=bus_pk)
        seat = get_object_or_404(Seat, pk=seat_id)

        print(seat.status, 'seat status')
        if seat.status == 'reserved':
            return Response({'message': 'Selected seat is reserved.'}, status=status.HTTP_400_BAD_REQUEST)
        
        booking = Booking.objects.create(user=user,bus=bus,route=route)
        booking.seats.set([seat])
        seat.status = 'reserved'
        seat.save()

        reponse = {
            "message":"booking created succcesfully",
            "booking_id": booking.pk,
        }
        return Response(reponse, status=status.HTTP_201_CREATED)
        # later on we  can also handle payment and other booking-related steps.

        # user = self.request.user

        # # Get bus, route, and seat IDs from the request data
        # bus_number= request.data.get('bus')
        # route = request.data.get('route')
        # seat_id = request.data.get('seats')

        # # Check if the bus, route, and seats exist
        # bus = Bus.objects.filter(bus_number =  bus_number)
        # # route = get_object_or_404(BusRoute, pk =route_id)
        # seats = Seat.objects.filter(pk=seat_id)

        # # Check if the selected seats are available and do not exceed the bus's capacity
        # unavailable_seats = seats.filter(status= 'reserved')
        # if unavailable_seats.exists() or len(seats)> bus.capacity:
        #     return Response({'message': 'Selected seats are not available or exceed the bus capacity.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Create a new booking
        # booking = Booking.objects.create(user=user, bus=bus, route=route)
        # booking.seats.set(seats)

        #  # Update seat statuses to 'reserved'
        # seats.update(status = 'reserved')



        # serializer= self.get_serializer(booking)

        # response_data = {
        #     'message': 'Booking created successfully',
        #     'data':serializer.data
        # }
        # return Response(response_data, status=status.HTTP_201_CREATED)

# Retrieve Booking View# Retrieve Booking View
class BookingDetailView(generics.RetrieveDestroyAPIView):
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
            "data": serializer.data,
            "username": request.user.username

        }

        return Response(response, status=status.HTTP_200_OK)

# Booking Confirm View
class BookingConfirmView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    pagination_class = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
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


# bus logics

class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serialzer = self.get_serializer(data= request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response({'message': 'Bus created successfully', "data":serialzer.data}, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]  # Restrict to admin users

    def retrieve(self, request, *args, **kwargs):
        bus_id = kwargs.get('pk')

        # Check if the bus exists, or return a 404 response
        bus = get_object_or_404(Bus, pk=bus_id)

        serializer = self.get_serializer(bus)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusSearchView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'departure_location': ['exact'],
        'arrival_location': ['exact'],
    }

    def get_queryset(self):
        # Get the 'departure_location' and 'arrival_location' parameters from the query string
        departure_location = self.request.GET.get('departure_location')
        arrival_location = self.request.GET.get('arrival_location')

        # Use these parameters to filter the queryset
        queryset = Bus.objects.all()

        if departure_location:
            queryset = queryset.filter(departure_location__icontains=departure_location)
        if arrival_location:
            queryset = queryset.filter(arrival_location__icontains=arrival_location)

        return queryset

## seat logics 
class SeatListView(generics.ListAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class SeatDetailView(generics.RetrieveAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
  
class SeatListForBusView(generics.ListAPIView):
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        bus_id = self.kwargs['bus_id']  # Get the bus ID from the URL parameter
        return Seat.objects.filter(bus__id=bus_id)

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

