from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Flight, Booking
from django.contrib.auth.models import User
from booking.forms import FlightForm
from django.contrib.auth import authenticate, login, logout
from booking.models import Booking
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='/adminpanel/login/')(view_func)

def admin_login(request):

    error = ""

    if request.method == 'POST':

        username = request.POST.get('username', '')

        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            login(request, user)

            return redirect(
                '/adminpanel/'
            )

        else:

            error = "Invalid Admin Login"

    return render(
        request,
        'adminpanel/admin_login.html',
        {
            'error': error
        }
    )

def admin_forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get(
            'email'
        )

        try:

            user = User.objects.filter(
                email=email,
                is_superuser=True
            ).first()

            if user is None:
                raise User.DoesNotExist

            request.session[
                'reset_admin_id'
            ] = user.id

            return redirect(
                'admin_reset_password'
            )

        except User.DoesNotExist:

            messages.error(

                request,

                'Admin email not found'
            )

    return render(
        request,
        'adminpanel/admin_forgot_password.html'
    )

def admin_reset_password(request):

    admin_id = request.session.get(
        'reset_admin_id'
    )

    if not admin_id:

        return redirect(
            'admin_forgot_password'
        )

    if request.method == 'POST':

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password == confirm_password:

            admin = User.objects.get(
                id=admin_id
            )

            admin.set_password(
                password
            )

            admin.save()

            del request.session[
                'reset_admin_id'
            ]

            return redirect(
                'admin_login'
            )

    return render(
        request,
        'adminpanel/admin_reset_password.html'
    )

def admin_logout(request):

    logout(request)

    return redirect(
        '/adminpanel/login/'
    )

@superuser_required
def admin_dashboard(request):

    # TOTALS

    flights = Flight.objects.count()

    users = User.objects.filter(
        is_superuser=False
    ).count()

    total_bookings = Booking.objects.count()

    confirmed_bookings = Booking.objects.filter(
        status='Confirmed'
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status='Cancelled'
    ).count()

    # TODAY

    today = timezone.now().date()

    today_bookings = Booking.objects.filter(
        booking_date__date=today
    ).count()

    # YESTERDAY

    yesterday = today - timedelta(days=1)

    yesterday_bookings = Booking.objects.filter(
        booking_date__date=yesterday
    ).count()

    # LAST 7 DAYS

    last_7_days = today - timedelta(days=7)

    weekly_bookings = Booking.objects.filter(
        booking_date__date__gte=last_7_days
    ).count()

    return render(
        request,
        'adminpanel/dashboard.html',
        {
            'flights': flights,
            'users': users,
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'today_bookings': today_bookings,
            'yesterday_bookings': yesterday_bookings,
            'weekly_bookings': weekly_bookings,
        }
    )

# MANAGE FLIGHTS
@superuser_required
def manage_flights(request):

    flights = Flight.objects.all()

    return render(
        request,
        'adminpanel/manage_flights.html',
        {
            'flights': flights
        }
    )

# ADD FLIGHT
@superuser_required
def add_flight(request):

    form = FlightForm()

    if request.method == 'POST':

        form = FlightForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'manage_flights'
            )

    return render(
        request,
        'adminpanel/add_flight.html',
        {
            'form': form
        }
    )

# EDIT FLIGHT
@superuser_required
def edit_flight(request, id):

    flight = get_object_or_404(
        Flight,
        id=id
    )

    form = FlightForm(
        instance=flight
    )

    if request.method == 'POST':

        form = FlightForm(
            request.POST,
            instance=flight
        )

        if form.is_valid():

            form.save()

            return redirect(
                'manage_flights'
            )

    return render(
        request,
        'adminpanel/edit_flight.html',
        {
            'form': form
        }
    )

# DELETE FLIGHT
@superuser_required
def delete_flight(request, id):

    flight = get_object_or_404(
        Flight,
        id=id
    )

    flight.delete()

    return redirect(
        'manage_flights'
    )

@superuser_required
def manage_bookings(request):

    bookings = Booking.objects.all()

    return render(
        request,
        'adminpanel/manage_bookings.html',
        {
            'bookings': bookings
        }
    )

@superuser_required
def ticket_details(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    return render(

        request,

        'adminpanel/ticket_details.html',

        {

            'booking':
            booking

        }

    )

# USERS
@superuser_required
def manage_users(request):

    users = User.objects.filter(
        is_superuser=False
    )

    return render(
        request,
        'adminpanel/manage_users.html',
        {
            'users': users
        }
    )

@superuser_required
def delete_user(request, id):

    user = get_object_or_404(
        User,
        id=id
    )

    user.delete()

    return redirect(
        'manage_users'
    )

@superuser_required
def user_bookings(request, id):

    user = get_object_or_404(
        User,
        id=id
    )

    bookings = Booking.objects.filter(
        user=user
    )

    return render(
        request,
        'adminpanel/user_bookings.html',
        {
            'user_data': user,
            'bookings': bookings
        }
    )

@superuser_required
def admin_change_password(request):

    if not request.user.is_superuser:

        return redirect('/')

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
                "Password Changed Successfully"
            )

            return redirect(
                'admin_change_password'
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'adminpanel/change_password.html',
        {
            'form': form
        }
    )