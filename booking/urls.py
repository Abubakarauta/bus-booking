from django.urls import path 
from .views import *


urlpatterns = [
    #bus 
    path('admin/buses/', BusListCreateView.as_view(), name='admin-bus-list-create'),
    path('admin/buses/<int:pk>/', BusDetailView.as_view(), name='admin-bus-detail'),
    path('bus/<int:bus_id>/seats/', SeatListForBusView.as_view(), name='bus-seat-list'),


    #stops
    path('stops/', StopListCreateView.as_view(), name='stop-list-create'),
    path('stops/<int:pk>/', StopDetailView.as_view(), name='stop-detail'),

    #routes
    path('routes/', BusRouteListCreateView.as_view(), name='bus-route-list-create'),
    path('routes/<int:pk>/', BusRouteDetail.as_view(), name='Bus-route-detail'),
    path('routes/search/', BusRouteSearchView.as_view(), name='route-search' ),
    
    #booking
   
    path('bookings/', BookingCreateView.as_view(), name='bus-booking-create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='bus-booking-detail'),
    path('bookings/<int:pk>/confirm/', BookingConfirmView.as_view(), name='bus-booking-confirm'),
    path('bookings/history/', BookingHistoryView.as_view(), name='booking-history'),


    #seat
    path('seat/', SeatListView.as_view(), name='seat-list'),
    path('seat/<int:pk>/', SeatDetailView.as_view(), name='seat-detail'),

    #reservation
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),

    
    # Payment URL
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),

 
]