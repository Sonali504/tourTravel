from django.urls import path
from .views import * 
from . import views

app_name = 'tour'

urlpatterns = [
    path('', home, name='home'),
    path('tour/<int:tour_id>/', tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/book/', book_tour, name='book_tour'),
    path('tours/', tour_list, name='tour_list'),
    path("inquiry/", inquiry_view, name="inquiry"),
    path("registration/", RegistrationView.as_view(), name="registration"),  # Use the class-based view
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),  # Assuming you have a CustomerLogoutView class
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),  # Use the class-based view
    path('forget-password/', views.forget_password, name='forgetpassword'),
    path('profile/', CustomerProfileView.as_view(), name='customerprofile'),

]
