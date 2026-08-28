
import json
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Flight, Booking
from .forms import RegisterForm
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .forms import UpdateProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    PasswordChangeForm
)

from django.contrib.auth import (
    update_session_auth_hash
)

from django.contrib import messages


def landing_page(request):

    return render(
        request,
        'landing.html'
    )

def home(request):

    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()

    flight_list = Flight.objects.all().order_by('-id')

    if source:
        flight_list = flight_list.filter(source__icontains=source)
    if destination:
        flight_list = flight_list.filter(destination__icontains=destination)

    paginator = Paginator(flight_list, 5)   # 5 flights per page
    page_number = request.GET.get('page')
    flights = paginator.get_page(page_number)

    return render(
        request,
        'home.html',
        {
            'flights': flights,
            'source': source,
            'destination': destination
        }
    )

def user_login(request):

    error = ""

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        )

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # NORMAL USER ONLY

        if user is not None and not user.is_superuser:

            login(request, user)

            return redirect(
                'home'
            )

        else:

            error = "Invalid Login Credentials"

    return render(
        request,
        'login.html',
        {
            'error': error
        }
    )

from django.contrib import messages


def register(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                'Registration Successful!'
            )

            return redirect(
                'login'
            )

    return render(

        request,

        'register.html',

        {

            'form': form

        }

    )




def forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get(
            'email'
        )

        try:

            user = User.objects.filter(
                email=email,
                is_superuser=False
            ).first()

            if user is None:
                raise User.DoesNotExist

            request.session[
                'reset_user_id'
            ] = user.id

            return redirect(
                'reset_password'
            )

        except User.DoesNotExist:

            messages.error(

                request,

                'User email not found'
            )

    return render(
        request,
        'forgot_password.html'
    )

def reset_password(request):

    user_id = request.session.get(
        'reset_user_id'
    )

    if not user_id:

        return redirect(
            'forgot_password'
        )

    if request.method == 'POST':

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password == confirm_password:

            user = User.objects.get(
                id=user_id
            )

            user.set_password(
                password
            )

            user.save()

            del request.session[
                'reset_user_id'
            ]

            return redirect(
                'login'
            )

        else:

            messages.error(

                request,

                'Passwords do not match'
            )

    return render(
        request,
        'reset_password.html'
    )

def generate_seats(prefix, count):

    seats = []

    for i in range(1, count + 1):

        seats.append(f"{prefix}{i}")

    return seats




@login_required
def book_flight(request, id):

    flight = get_object_or_404(
        Flight,
        id=id
    )

    # GET ALREADY BOOKED SEATS

    booked_seats = []

    bookings = Booking.objects.filter(
    flight=flight
).exclude(
    status='Cancelled'
)

    for booking in bookings:

        seats = booking.seat_numbers.split(",")

        for seat in seats:

            booked_seats.append(
                seat.strip()
            )

    # BOOKING

    if request.method == 'POST':

        # Seats

        seat_numbers_str = request.POST.get(
            'seat_numbers',
            ''
        ).strip()

        if not seat_numbers_str:
            return render(request, 'book.html', {

                'flight': flight,

                'error': 'Please select at least one seat.',

                'booked_seats': booked_seats,

                'first_class_seats':
                    generate_seats(
                        "F",
                        flight.first_class_seats
                    ),

                'business_class_seats':
                    generate_seats(
                        "B",
                        flight.business_seats
                    ),

                'premium_class_seats':
                    generate_seats(
                        "P",
                        flight.premium_seats
                    ),

                'economy_class_seats':
                    generate_seats(
                        "E",
                        flight.economy_seats
                    ),
            })

        seat_numbers = seat_numbers_str.split(",")

        # Prevent duplicate booking

        for seat in seat_numbers:

            if seat.strip() in booked_seats:

                return render(request,
                    'book.html',
                    {
                        'flight': flight,
                        'error':
                        f"Seat {seat} is already booked.",

                        'booked_seats':
                            booked_seats,

                        'first_class_seats':
                            generate_seats(
                                "F",
                                flight.first_class_seats
                            ),

                        'business_class_seats':
                            generate_seats(
                                "B",
                                flight.business_seats
                            ),

                        'premium_class_seats':
                            generate_seats(
                                "P",
                                flight.premium_seats
                            ),

                        'economy_class_seats':
                            generate_seats(
                                "E",
                                flight.economy_seats
                            ),
                    }
                )

        # Classes JSON

        travel_class_json = request.POST.get(
            'travel_class',
            '{}'
        )

        try:
            travel_classes = json.loads(
                travel_class_json
            )
        except json.JSONDecodeError:

            return render(request, 'book.html', {

                'flight': flight,

                'error': 'Please select at least one seat.',

                'booked_seats': booked_seats,

                'first_class_seats':
                    generate_seats(
                        "F",
                        flight.first_class_seats
                    ),

                'business_class_seats':
                    generate_seats(
                        "B",
                        flight.business_seats
                    ),

                'premium_class_seats':
                    generate_seats(
                        "P",
                        flight.premium_seats
                    ),

                'economy_class_seats':
                    generate_seats(
                        "E",
                        flight.economy_seats
                    ),
            })

        # Passenger details

        passenger_names = request.POST.getlist(
            'passenger_name[]'
        )

        passenger_ages = request.POST.getlist(
            'passenger_age[]'
        )

        passenger_genders = request.POST.getlist(
            'passenger_gender[]'
        )

        # Total amount

        total_amount = 0

        # Class list

        class_list = []

        # Passenger combined info

        passenger_info = []

        for i in range(len(seat_numbers)):

            seat = seat_numbers[i]

            seat_class = travel_classes[
                seat
            ]

            class_list.append(
                seat_class
            )

            # PRICE BY CLASS

            if seat_class == "Economy":

                price = flight.economy_price

            elif seat_class == "Premium Economy":

                price = flight.premium_price

            elif seat_class == "Business":

                price = flight.business_price

            else:

                price = flight.first_price

            total_amount += price

            passenger_info.append(

                f"{passenger_names[i]}"
                f" ({passenger_ages[i]}/"
                f"{passenger_genders[i]})"

            )

        # CREATE BOOKING

        Booking.objects.create(

            user=request.user,

            flight=flight,

            passenger_name=
                ", ".join(passenger_info),

            passenger_age="-",

            passenger_gender="-",

            seat_numbers=
                ", ".join(seat_numbers),

            travel_class=
                ", ".join(class_list),

            total_amount=
                total_amount

        )

        # REDUCE AVAILABLE SEATS

        flight.available_seats -= len(
            seat_numbers
        )

        flight.save()

        return redirect('/my-bookings/')

    # PAGE LOAD

    return render(request, 'book.html', {

        'flight': flight,

        'booked_seats':
            booked_seats,

        'first_class_seats':

            generate_seats(
                "F",
                flight.first_class_seats
            ),

        'business_class_seats':

            generate_seats(
                "B",
                flight.business_seats
            ),

        'premium_class_seats':

            generate_seats(
                "P",
                flight.premium_seats
            ),

        'economy_class_seats':

            generate_seats(
                "E",
                flight.economy_seats
            ),

    })



@login_required
def my_bookings(request):

    booking_list = Booking.objects.filter(
        user=request.user
    ).order_by('-id')

    paginator = Paginator(
        booking_list,
        4
    )

    page_number = request.GET.get('page')

    bookings = paginator.get_page(
        page_number
    )

    return render(request,
        'my_bookings.html',
        {
            'bookings': bookings
        }
    )

@login_required
def boarding_pass(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    return render(
        request,
        'boarding_pass.html',
        {
            'b': booking
        }
    )


@login_required
def cancel_booking(request, id):

    # Superuser/admin can cancel any booking, normal users can only cancel their own
    if request.user.is_superuser:
        booking = get_object_or_404(
            Booking,
            id=id
        )
    else:
        booking = get_object_or_404(
            Booking,
            id=id,
            user=request.user
        )

    departure_time = booking.flight.departure_time

    # ONLY BEFORE 1 DAY
    if timezone.now() < departure_time - timedelta(days=1):
        # UPDATE STATUS
        booking.status = "Cancelled"
        booking.save()

        messages.success(
            request,
            "Ticket Cancelled Successfully"
        )
    else:
        messages.error(
            request,
            "Cancellation closed."
        )

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)

    if request.user.is_superuser:
        return redirect('manage_bookings')
    return redirect('my_bookings')


@login_required
def user_profile(request):

    if request.method == 'POST':

        form = UpdateProfileForm(

            request.POST,

            instance=request.user

        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile Updated Successfully"
            )

            return redirect(
                'user_profile'
            )

    else:

        form = UpdateProfileForm(
            instance=request.user
        )

    return render(
        request,
        'profile.html',
        {
            'form': form
        }
    )

@login_required

def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(

            request.user,

            request.POST

        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(

                request,

                user

            )

            messages.success(

                request,

                'Password Changed Successfully'

            )

            form = PasswordChangeForm(
                request.user
            )

        else:

            # Current password wrong

            if form.errors.get(
                'old_password'
            ):

                messages.error(

                    request,

                    'Current Password is Incorrect'

                )

            # Password mismatch

            elif form.errors.get(
                'new_password2'
            ):

                messages.error(

                    request,

                    'New Password and Confirm Password do not match'

                )

            else:

                messages.error(

                    request,

                    'Please correct the errors'

                )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(

        request,

        'change_password.html',

        {

            'form': form

        }

    )

def user_logout(request):

    logout(request)

    return redirect('/login/')