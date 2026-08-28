
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path(
        '',
        views.landing_page,
        name='landing_page'
    ),
    path('home', views.home, name='home'),
    path('register/', views.register, name='register'),
   path(
    'login/',
    views.user_login,
    name='login'

),
path(
    'forgot-password/',
    views.forgot_password,
    name='forgot_password'
),
path(
    'reset-password/',
    views.reset_password,
    name='reset_password'
),
    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path('book/<int:id>/', views.book_flight, name='book_flight'),
    path('my-bookings/', views.my_bookings,name='my_bookings'),
    path(
    'boarding-pass/<int:id>/',
    views.boarding_pass,
    name='boarding_pass'
),
path(
    'cancel-booking/<int:id>/',
    views.cancel_booking,
    name='cancel_booking'
),
path(
    'profile/',
    views.user_profile,
    name='user_profile'
),

path(
    'change-password/',
    views.change_password,
    name='change_password'
),
 path(
        'adminpanel/',
        include('adminpanel.urls')
    ),
]

