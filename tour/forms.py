from django import forms
from .models import Booking
from .models import *
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget(), label="Start Date")
    end_date = forms.DateField(widget=forms.SelectDateWidget(), label="End Date")
    tour_price = forms.DecimalField(label="Price per person per day", max_digits=10, decimal_places=2, disabled=True, required=False)
    num_people = forms.IntegerField(label="Number of People", initial=1, min_value=1)

    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'start_date', 'end_date', 'num_people']

    def __init__(self, *args, **kwargs):
        self.tour = kwargs.pop('tour', None)
        super().__init__(*args, **kwargs)
        if self.tour:
            # Pre-fill tour price and add date information as help text
            self.fields['tour_price'].initial = self.tour.price
            self.fields['num_people'].initial = 1
            self.fields['start_date'].help_text = f"Available from {self.tour.start_date.strftime('%Y-%m-%d')} to {self.tour.end_date.strftime('%Y-%m-%d')}"
            self.fields['end_date'].help_text = f"Available until {self.tour.end_date.strftime('%Y-%m-%d')}"

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        num_people = cleaned_data.get('num_people')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date must be after the start date.")
            if self.tour and (start_date < self.tour.start_date or end_date > self.tour.end_date):
                raise forms.ValidationError("Selected dates must be within the tour's available dates.")
        
        if self.tour and num_people:
            total_price = self.tour.price * num_people * (end_date - start_date).days
            cleaned_data['total_price'] = total_price

        return cleaned_data

class InquiryForm(forms.Form):
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), required=True)
    start_date = forms.DateField(widget=forms.SelectDateWidget, required=True)
    end_date = forms.DateField(widget=forms.SelectDateWidget, required=True)
    num_people = forms.IntegerField(min_value=1, required=True)
    email = forms.EmailField(required=True)
    
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ["username", "full_name", "email", "password"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():  # Corrected here
            raise forms.ValidationError("*Customer already exists.*")
        return uname

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())  