
from django.contrib import admin
from .models import Flight, Booking

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_name',
        'flight_no',
        'source',
        'destination'
    ]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'passenger_name',
        'flight',
        'seat_numbers',
        'travel_class',
        'total_amount'
    ]

