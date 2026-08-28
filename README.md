# AeroReserve

AeroReserve is a premium web-based Airline Reservation and Booking System built with Django and styled with a modern, glassmorphic layout. It provides a complete booking lifecycle for users and an administration interface for reservation management.

## 🚀 Features

### For Users
- **Flight Discovery**: Search and filter flights by departure/arrival cities.
- **Interactive Seat Selection**: Visual cabin seat layout with class-specific seat configurations (First Class, Business, Premium Economy, and Economy).
- **Dynamic Bookings**: Input multiple passenger names, ages, and genders for a single reservation.
- **Boarding Passes**: Generate virtual boarding passes with seat details and QR/ticket numbers.
- **Hassle-free Cancellations**: Cancel tickets up to 24 hours before departure with automated seat restoration.

### For Administrators
- **Dashboard Metrics**: Real-time stats on flights, active users, bookings (today, yesterday, and weekly), and confirmation/cancellation rates.
- **Flight Management**: Add, update, and remove flights.
- **Booking Audits**: Track and cancel reservations system-wide.
- **User Management**: View users, audit their bookings, or remove accounts.

---

## 🛠️ Technology Stack
- **Backend**: Django 5.x, Python 3.x
- **Database**: SQLite3 (local development)
- **Frontend**: HTML5, CSS3 (Vanilla / Custom Flexbox & Grid), Bootstrap 5, FontAwesome 6

---

## 💻 Setup and Installation

### Prerequisites
- Python 3.10 or higher
- Git

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/amanrobinsonthakur/AeroReserve-.git
   cd AeroReserve-
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate # On Unix/macOS
   ```

3. **Install Dependencies**
   ```bash
   pip install django
   ```

4. **Run Database Migrations**
   ```bash
   python Scripts/manage.py migrate
   ```

5. **Start Development Server**
   ```bash
   $env:PYTHONPATH="."
   python Scripts/manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Testing
Run the automated test suite to verify code correctness:
```bash
$env:PYTHONPATH="."
python Scripts/manage.py test
```
