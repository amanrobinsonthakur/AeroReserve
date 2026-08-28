from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Flight, Booking

class AirlineBookingSystemTests(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Password123"
        )
        
        # Create a flight
        self.flight = Flight.objects.create(
            flight_name="Test Indigo",
            flight_no="6E-101",
            source="Delhi",
            destination="Mumbai",
            departure_time=timezone.now() + timedelta(days=2),
            arrival_time=timezone.now() + timedelta(days=2, hours=2),
            economy_seats=10,
            premium_seats=5,
            business_seats=5,
            first_class_seats=2,
            economy_price=1000.00,
            premium_price=2000.00,
            business_price=3000.00,
            first_price=5000.00
        )

    def test_flight_initial_seats(self):
        """Verify that total seats and available seats are calculated correctly on creation."""
        self.assertEqual(self.flight.total_seats, 22) # 10 + 5 + 5 + 2
        self.assertEqual(self.flight.available_seats, 22)

    def test_booking_reduces_available_seats(self):
        """Verify that creating a booking successfully decrements the available seats on the flight."""
        booking = Booking.objects.create(
            user=self.user,
            flight=self.flight,
            passenger_name="Alice (25/Female), Bob (30/Male)",
            passenger_age="-",
            passenger_gender="-",
            seat_numbers="E1, E2",
            travel_class="Economy, Economy",
            total_amount=2000.00
        )
        
        # Save flight to trigger available seats updates
        self.flight.save()
        
        # Re-fetch flight from database
        self.flight.refresh_from_db()
        
        # Initial seats was 22, booked 2 seats (E1, E2). Available seats should be 20.
        self.assertEqual(self.flight.available_seats, 20)

    def test_cancelled_booking_restores_available_seats(self):
        """Verify that cancelling a booking restores the available seats on the flight."""
        booking = Booking.objects.create(
            user=self.user,
            flight=self.flight,
            passenger_name="Alice (25/Female)",
            passenger_age="-",
            passenger_gender="-",
            seat_numbers="F1",
            travel_class="First Class",
            total_amount=5000.00
        )
        
        self.flight.save()
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 21) # 22 - 1
        
        # Cancel the booking
        booking.status = "Cancelled"
        booking.save()
        
        # Recalculate available seats by saving the flight again (similar to views.py cancel flow)
        self.flight.save()
        self.flight.refresh_from_db()
        
        # Available seats should be restored back to 22
        self.assertEqual(self.flight.available_seats, 22)

    def test_flight_search(self):
        """Verify that the search functionality on the homepage works correctly."""
        # Create a second flight with a different route
        Flight.objects.create(
            flight_name="Test Air India",
            flight_no="AI-202",
            source="London",
            destination="New York",
            departure_time=timezone.now() + timedelta(days=5),
            arrival_time=timezone.now() + timedelta(days=5, hours=8),
            economy_seats=15,
            premium_seats=5,
            business_seats=5,
            first_class_seats=2,
            economy_price=40000.00,
            premium_price=60000.00,
            business_price=120000.00,
            first_price=250000.00
        )
        
        # 1. Search for Delhi source
        response = self.client.get('/home', {'source': 'Delhi'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['flights']), 1)
        self.assertEqual(response.context['flights'][0].flight_name, "Test Indigo")

        # 2. Search for London source
        response = self.client.get('/home', {'source': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['flights']), 1)
        self.assertEqual(response.context['flights'][0].flight_name, "Test Air India")

        # 3. Search for non-existent source
        response = self.client.get('/home', {'source': 'Paris'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['flights']), 0)

    def test_admin_can_cancel_any_booking(self):
        """Verify that a superuser admin can cancel bookings belonging to other users."""
        # Create user's booking
        booking = Booking.objects.create(
            user=self.user,
            flight=self.flight,
            passenger_name="User Passenger",
            passenger_age="-",
            passenger_gender="-",
            seat_numbers="E1",
            travel_class="Economy",
            total_amount=1000.00
        )
        
        # Create an admin superuser
        admin = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="AdminPassword123"
        )
        
        # Log in as admin
        self.client.login(username="adminuser", password="AdminPassword123")
        
        # Cancel booking as admin
        response = self.client.get(f'/cancel-booking/{booking.id}/')
        
        # Verify redirect occurred (meaning it did not raise a 404)
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "Cancelled")

    def test_user_cannot_cancel_others_booking(self):
        """Verify that a regular user cannot cancel a booking belonging to another user (should return 404)."""
        # Create another regular user
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="Password123"
        )
        
        # Create other_user's booking
        booking = Booking.objects.create(
            user=other_user,
            flight=self.flight,
            passenger_name="Other Passenger",
            passenger_age="-",
            passenger_gender="-",
            seat_numbers="E1",
            travel_class="Economy",
            total_amount=1000.00
        )
        
        # Log in as self.user (not other_user)
        self.client.login(username="testuser", password="Password123")
        
        # Try to cancel booking belonging to other_user
        response = self.client.get(f'/cancel-booking/{booking.id}/')
        
        # Should raise a 404
        self.assertEqual(response.status_code, 404)
        booking.refresh_from_db()
        self.assertNotEqual(booking.status, "Cancelled")

    def test_admin_views_require_superuser(self):
        """Verify that admin dashboard redirects non-superusers."""
        # Log in as a regular user
        self.client.login(username="testuser", password="Password123")
        
        # Access admin dashboard
        response = self.client.get('/adminpanel/')
        
        # Should redirect to login_url '/adminpanel/login/'
        self.assertRedirects(response, '/adminpanel/login/?next=/adminpanel/')

    def test_booking_signals_recalculate_seats(self):
        """Verify that signals automatically recalculate flight seats on save and cascade deletion."""
        # Initial seats: 22
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 22)
        
        # Create booking (triggers post_save signal)
        booking = Booking.objects.create(
            user=self.user,
            flight=self.flight,
            passenger_name="Alice (25/Female)",
            passenger_age="-",
            passenger_gender="-",
            seat_numbers="F1",
            travel_class="First Class",
            total_amount=5000.00
        )
        
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 21) # 22 - 1
        
        # Cancel booking (triggers post_save signal)
        booking.status = "Cancelled"
        booking.save()
        
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 22) # restored
        
        # Reactivate booking
        booking.status = "Confirmed"
        booking.save()
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 21)
        
        # Delete booking directly (triggers post_delete signal)
        booking.delete()
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 22) # restored again
        
        # Cascade delete (deleting user deletes bookings via cascade, which triggers signals)
        user2 = User.objects.create_user(username="user2", password="password")
        booking2 = Booking.objects.create(
            user=user2,
            flight=self.flight,
            passenger_name="Bob (30/Male)",
            passenger_age="-",
            passenger_gender="-",
            seat_numbers="B1, B2",
            travel_class="Business, Business",
            total_amount=6000.00
        )
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 20) # 22 - 2
        
        # Deleting user2 cascade-deletes booking2
        user2.delete()
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.available_seats, 22) # restored via cascade-delete signals

