from django.db import models
from django.conf import settings

class Trip(models.Model):
    SEASON_CHOICES = (
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
    )
    DESTINATION_TYPE_CHOICES = (
        ('mountains', 'Mountains'),
        ('beaches', 'Beaches'),
        ('deserts', 'Deserts'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, blank=True)
    destination_type = models.CharField(max_length=20, choices=DESTINATION_TYPE_CHOICES, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, blank=True, default="")
    is_available = models.BooleanField(default=True)
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_trips',
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='trip_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Booking(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='bookings')
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_persons = models.PositiveIntegerField(default=1)
    departure_date = models.DateField()

    def __str__(self):
        return f"{self.traveler.full_name} booked {self.trip.title} for {self.departure_date}"

