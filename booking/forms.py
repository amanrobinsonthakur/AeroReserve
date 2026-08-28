
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Flight



class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = [

            'username',
            'email',
            'password1',
            'password2'

        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs['class'] = 'form-control'




class FlightForm(forms.ModelForm):

    class Meta:

        model = Flight

        fields = '__all__'

        widgets = {

            # FLIGHT DETAILS

            'flight_name': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Enter Flight Name'

                }

            ),

            'flight_no': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Enter Flight Number'

                }

            ),

            # ROUTE

            'source': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Departure City'

                }

            ),

            'destination': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Arrival City'

                }

            ),

            # DATE & TIME

            'departure_time': forms.DateTimeInput(

                attrs={

                    'type': 'datetime-local',

                    'class': 'form-control'

                }

            ),

            'arrival_time': forms.DateTimeInput(

                attrs={

                    'type': 'datetime-local',

                    'class': 'form-control'

                }

            ),

            # SEATS

            'total_seats': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Total Seats'

                }

            ),

            'available_seats': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Available Seats'

                }

            ),

            'first_class_seats': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'First Class Seats'

                }

            ),

            'business_seats': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Business Class Seats'

                }

            ),

            'premium_seats': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Premium Economy Seats'

                }

            ),

            'economy_seats': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Economy Seats'

                }

            ),

            # PRICES

            'first_price': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'First Class Price'

                }

            ),

            'business_price': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Business Class Price'

                }

            ),

            'premium_price': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Premium Economy Price'

                }

            ),

            'economy_price': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Economy Price'

                }

            ),

        }

    # CUSTOM LABELS

    labels = {

        'flight_name': 'Flight Name',

        'flight_no': 'Flight Number',

        'source': 'Source Airport',

        'destination': 'Destination Airport',

        'departure_time': 'Departure Date & Time',

        'arrival_time': 'Arrival Date & Time',

        'total_seats': 'Total Seats',

        'available_seats': 'Available Seats',

        'first_class_seats': 'First Class Seats',

        'business_seats': 'Business Class Seats',

        'premium_seats': 'Premium Economy Seats',

        'economy_seats': 'Economy Seats',

        'first_price': 'First Class Price',

        'business_price': 'Business Class Price',

        'premium_price': 'Premium Economy Price',

        'economy_price': 'Economy Price',

    }



class UpdateProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [

            'first_name',
            'last_name',
            'username',
            'email'

        ]

        widgets = {

            'first_name': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'First Name'

                }

            ),

            'last_name': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Last Name'

                }

            ),

            'username': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Username'

                }

            ),

            'email': forms.EmailInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': 'Email Address'

                }

            ),

        }