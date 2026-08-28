from django.db import models

from django.contrib.auth.models import User

import random
import string


CLASS_CHOICES = (

    ('Economy', 'Economy'),

    ('Premium Economy', 'Premium Economy'),

    ('Business', 'Business'),

    ('First Class', 'First Class'),

)


class Flight(models.Model):

    flight_name = models.CharField(
        max_length=100
    )

    flight_no = models.CharField(
        max_length=50
    )

    source = models.CharField(
        max_length=100
    )

    destination = models.CharField(
        max_length=100
    )

    departure_time = models.DateTimeField()

    arrival_time = models.DateTimeField()

    # Seats

    economy_seats = models.IntegerField()

    premium_seats = models.IntegerField()

    business_seats = models.IntegerField()

    first_class_seats = models.IntegerField()

    # Auto Total

    total_seats = models.IntegerField(
        editable=False,
        default=0
    )

    available_seats = models.IntegerField(
        editable=False,
        default=0
    )

    # Prices

    economy_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    premium_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    business_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    first_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):

        self.total_seats = (

            self.economy_seats +

            self.premium_seats +

            self.business_seats +

            self.first_class_seats

        )

        if not self.pk:
            self.available_seats = self.total_seats
        else:
            bookings = self.booking_set.exclude(status='Cancelled')
            booked_count = 0
            for b in bookings:
                booked_count += len([s for s in b.seat_numbers.split(',') if s.strip()])
            self.available_seats = self.total_seats - booked_count

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            self.flight_name +
            " - " +
            self.flight_no
        )


class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    ticket_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE
    )

    passenger_name = models.TextField()

    passenger_age = models.TextField()

    passenger_gender = models.TextField()

    seat_numbers = models.TextField()

    travel_class = models.TextField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    payment_status = models.CharField(
        max_length=20,
        default='Paid'
    )
    status = models.CharField(
    max_length=20,
    default='Confirmed'
)

    def save(self, *args, **kwargs):

        if not self.ticket_number:

            self.ticket_number = (

                "AIR" +

                ''.join(

                    random.choices(

                        string.digits,

                        k=8

                    )

                )

            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.ticket_number


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Booking)
def update_flight_seats_on_save(sender, instance, **kwargs):
    instance.flight.save()

@receiver(post_delete, sender=Booking)
def update_flight_seats_on_delete(sender, instance, **kwargs):
    instance.flight.save()