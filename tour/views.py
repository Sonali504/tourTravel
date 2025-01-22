from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, View
from django.contrib import messages
from .models import Tour, Destination, Customer
from .forms import BookingForm, InquiryForm, RegistrationForm, CustomerLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView

# Home page showing all tours
def home(request):
    tours = Tour.objects.all()[:3]  # Limit to the first three tours
    return render(request, 'home.html', {'tours': tours})

# Tour detail page showing individual tour information
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour_detail.html', {'tour': tour})

# Booking page for a specific tour
@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, tour=tour)  # Pass tour to form
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.save()
            return render(request, 'booking_success.html', {'tour': tour})
    else:
        form = BookingForm(tour=tour)
    return render(request, 'book_tour.html', {'form': form, 'tour': tour})

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'list-tour.html', {'tours': tours})

def inquiry_view(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Process form data or send inquiry
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            num_people = form.cleaned_data['num_people']
            email = form.cleaned_data['email']
            messages.success(request, "Your inquiry has been sent successfully.")
            return redirect("inquiry")
    else:
        form = InquiryForm()
    return render(request, "inquiry_form.html", {"form": form})

class RegistrationView(CreateView):
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("tour:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        # Create the User instance
        user = User.objects.create_user(username=username, email=email, password=password)

        # Associate the User with the Customer instance
        customer = form.save(commit=False)  # Don't save the form yet
        customer.user = user  # Set the user
        customer.save()  # Now save the Customer instance

        # Log in the user
        login(self.request, user)

        return super().form_valid(form)

class CustomerLoginView(View):
    template_name = "login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("tour:home")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pword = form.cleaned_data.get("password")
            usr = authenticate(username=uname, password=pword)
            if usr is not None and Customer.objects.filter(user=usr).exists():
                login(request, usr)
                return redirect(self.get_success_url())
            else:
                return render(request, self.template_name, {"form": form, "error": "Invalid credentials"})
        return render(request, self.template_name, {"form": form})

    def get_success_url(self):
        if "next" in self.request.GET:
            return self.request.GET["next"]
        return self.success_url
    
class CustomerProfileView(TemplateView):
    template_name = 'customer_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Add user details to the context
        return context    

# Optional logout functionality if you need a custom one
class CustomerLogoutView(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('tour:home')  # Redirect to home page after logout

def forget_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)  # Send reset link email
            return render(request, 'password_reset_done.html')  # Redirect after successful email send
    else:
        form = PasswordResetForm()

    return render(request, 'forget_password.html', {'form': form})