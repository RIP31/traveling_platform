from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip, Booking
from .forms import TripForm, BookingForm
from accounts.decorators import traveler_required, provider_required

def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'trips/trip_list.html', {'trips': trips})

def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    dummy_reviews = [
        {'reviewer': 'John Doe', 'comment': 'Had an amazing time exploring the scenic beauty. Highly recommend this trip!', 'rating': 5},
        {'reviewer': 'Sam Wilson', 'comment': 'Great itinerary and excellent service. Would book again!', 'rating': 5},
        {'reviewer': 'Emily Johnson', 'comment': 'A memorable journey with breathtaking views. Worth every penny.', 'rating': 3},
        {'reviewer': 'Jane Smith', 'comment': 'The trip was well organized, and the experience was unforgettable!', 'rating': 4},
    ]
    for review in dummy_reviews:
        review['stars'] = '★' * review['rating'] + '☆' * (5 - review['rating'])
    return render(request, 'trips/trip_detail.html', {'trip': trip, 'reviews': dummy_reviews})

def search_trips(request):
    trips = Trip.objects.filter(is_available=True)
    from_city = request.GET.get('from_city')
    to_city = request.GET.get('to_city')
    season = request.GET.get('season')
    destination_type = request.GET.get('destination_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if from_city:
        trips = trips.filter(from_city__icontains=from_city)
    if to_city:
        trips = trips.filter(to_city__icontains=to_city)
    if season:
        trips = trips.filter(season=season)
    if destination_type:
        trips = trips.filter(destination_type=destination_type)
    if min_price:
        try:
            trips = trips.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            trips = trips.filter(price__lte=float(max_price))
        except ValueError:
            pass

    return render(request, 'trips/search_result.html', {'trips': trips})


@login_required
@traveler_required
def booking_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user = request.user
            user.full_name = form.cleaned_data['full_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.save()

            # Validate the departure date against the trip's season
            departure_date = form.cleaned_data['departure_date']
            if trip.season == 'summer' and not (5 <= departure_date.month <= 8):
                form.add_error('departure_date', "This trip is only available in summer (May to August).")
            elif trip.season == 'winter' and not (12 <= departure_date.month or departure_date.month <= 2):
                form.add_error('departure_date', "This trip is only available in winter (December to February).")
            elif trip.season == 'monsoon' and not (7 <= departure_date.month <= 9):
                form.add_error('departure_date', "This trip is only available in monsoon (July to September).")
            else:
                Booking.objects.create(
                    trip=trip,
                    traveler=user,
                    number_of_persons=form.cleaned_data['number_of_persons'],
                    departure_date=departure_date
                )
                messages.success(request, "Your booking has been confirmed!")
                return redirect('dashboard')
    else:
        form = BookingForm(initial={
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone': request.user.phone,
            'number_of_persons': 1,
        })
    
    return render(request, 'trips/booking_details.html', {'form': form, 'trip': trip})


@login_required
@provider_required
def provider_dashboard(request):
    trips = Trip.objects.filter(provider=request.user)
    bookings = Booking.objects.filter(trip__in=trips)
    total_bookings = bookings.count()
    total_revenue = 0
    for trip in trips:
        if trip.price:
            trip_bookings = bookings.filter(trip=trip).count()
            total_revenue += trip.price * trip_bookings

    context = {
        'trips': trips,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
    }
    return render(request, 'trips/provider_dashboard.html', context)

@login_required
@provider_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.provider = request.user
            trip.save()
            messages.success(request, "Trip created successfully.")
            return redirect('provider_dashboard')
    else:
        form = TripForm()
    return render(request, 'trips/create_trip.html', {'form': form})

@login_required
@provider_required
def edit_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, provider=request.user)
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip updated successfully!")
            return redirect('provider_dashboard')
    else:
        form = TripForm(instance=trip)
    return render(request, 'trips/edit_trip.html', {'form': form, 'trip': trip})

@login_required
@provider_required
def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, provider=request.user)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, "Trip deleted successfully.")
        return redirect('provider_dashboard')
    return render(request, 'trips/delete_trip.html', {'trip': trip})


@login_required
def booking_detail(request, booking_id):
    # Allow admin users to see any booking, travelers to see only their own
    if request.user.role == 'admin':
        booking = get_object_or_404(Booking, pk=booking_id)
    else:
        booking = get_object_or_404(Booking, pk=booking_id, traveler=request.user)
    
    total_price = booking.trip.price * booking.number_of_persons
    
    if request.method == 'POST':
        # Only allow travelers to cancel their own bookings, or admins to cancel any booking
        if request.user.role == 'admin' or booking.traveler == request.user:
            booking.delete()
            messages.success(request, "Booking has been cancelled.")
            return redirect('dashboard')
        else:
            messages.error(request, "You don't have permission to cancel this booking.")
    
    return render(request, 'trips/booking_detail_view.html', {
        'booking': booking,
        'total_price': total_price,
    })