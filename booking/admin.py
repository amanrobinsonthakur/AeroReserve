
from django.contrib import admin
from .models import Flight, Booking

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_name',
        'flight_no',
        'source',
        'destination',
        'departure_time',
        'arrival_time',
        'total_seats',
        'available_seats'
    ]
    list_filter = ['source', 'destination', 'departure_time']
    search_fields = ['flight_name', 'flight_no', 'source', 'destination']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number',
        'passenger_name',
        'flight',
        'seat_numbers',
        'travel_class',
        'total_amount',
        'booking_date',
        'status'
    ]
    list_filter = ['travel_class', 'status', 'booking_date']
    search_fields = ['ticket_number', 'passenger_name', 'flight__flight_name', 'flight__flight_no']

