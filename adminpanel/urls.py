from django.urls import path
from . import views

urlpatterns = [
path(
    'login/',
    views.admin_login,
    name='admin_login'
),
path(
    'admin-forgot-password/',
    views.admin_forgot_password,
    name='admin_forgot_password'
),

path(
    'admin-reset-password/',
    views.admin_reset_password,
    name='admin_reset_password'
),
path(
    'logout/',
    views.admin_logout,
    name='admin_logout'
),
    path(
        '',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'flights/',
        views.manage_flights,
        name='manage_flights'
    ),

    path(
        'flights/add/',
        views.add_flight,
        name='add_flight'
    ),

    path(
        'flights/edit/<int:id>/',
        views.edit_flight,
        name='edit_flight'
    ),

    path(
        'flights/delete/<int:id>/',
        views.delete_flight,
        name='delete_flight'
    ),

    path(
        'bookings/',
        views.manage_bookings,
        name='manage_bookings'
    ),
    path(
    'ticket-details/<int:id>/',
    views.ticket_details,
    name='ticket_details'
),

    path(
        'users/',
        views.manage_users,
        name='manage_users'
    ),
    path(
    'users/delete/<int:id>/',
    views.delete_user,
    name='delete_user'
),

path(
    'users/bookings/<int:id>/',
    views.user_bookings,
    name='user_bookings'
),
path(
    'change-password/',
    views.admin_change_password,
    name='admin_change_password'
),

]