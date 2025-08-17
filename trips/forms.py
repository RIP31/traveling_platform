from django import forms
from .models import Trip
from datetime import date

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'title', 'description', 'from_city', 'to_city',
            'duration', 'season', 'destination_type', 
            'price', 'is_available', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter trip title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter trip description', 'class': 'form-control'}),
            'from_city': forms.TextInput(attrs={'placeholder': 'Enter departure city', 'class': 'form-control'}),
            'to_city': forms.TextInput(attrs={'placeholder': 'Enter destination city', 'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Enter destination city', 'class': 'form-control'}),
            'season': forms.Select(attrs={'placeholder': 'Select season', 'class': 'form-control'}),
            'destination_type': forms.Select(attrs={'placeholder': 'Select destination', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter trip price', 'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['from_city'].required = True
        self.fields['to_city'].required = True
        self.fields['duration'].required = True
        self.fields['price'].required = True
        self.fields['image'].required = True

class BookingForm(forms.Form):
    full_name = forms.CharField(
        max_length=150, 
        required=True, 
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15, 
        required=True, 
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'})
    )
    number_of_persons = forms.IntegerField(
        min_value=1, 
        required=True, 
        label="Number of Persons",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of persons', 'class': 'form-control'})
    )
    departure_date = forms.DateField(
        required=True,
        label="Departure Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    def clean_departure_date(self):
        departure_date = self.cleaned_data.get('departure_date')
        if departure_date < date.today():
            raise forms.ValidationError("Departure date cannot be in the past.")
        return departure_date
