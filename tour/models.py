from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')

    def __str__(self):
        return self.name

class Tour(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    tour_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/', null=True, blank=True)

    def __str__(self):
        return f"{self.tour_name} - {self.destination.name}"

class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{1,15}$', message="Enter a valid phone number (digits only).")]
    )
    tour_date = models.DateField(null=True, blank=True)
    num_people = models.PositiveIntegerField(default=1)
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.full_name} on {self.booking_date}"
