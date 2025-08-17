from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from trips.models import Booking
from django.contrib.auth.views import LoginView
from .decorators import *

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')  # Assumes a URL named 'login' exists
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error = "Invalid credentials"
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    # Allow admin users to see all bookings, travelers to see only their own
    if request.user.role == 'admin':
        bookings = Booking.objects.all().order_by('-booking_date')
    else:
        bookings = Booking.objects.filter(traveler=request.user).order_by('-booking_date')
    
    for booking in bookings:
        booking.total_price = booking.trip.price * booking.number_of_persons
    return render(request, 'accounts/dashboard.html', {'bookings': bookings})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirect based on user role
        if self.request.user.role == 'provider':
            return reverse_lazy('provider_dashboard')
        elif self.request.user.role == 'admin':
            return reverse_lazy('dashboard')  # Admin can access dashboard
        else:
            return reverse_lazy('dashboard')