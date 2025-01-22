from django.urls import path
from .views import *

app_name="ecomapp"
urlpatterns = [
    path("", HomeViews.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contact-us/', ContactUsView.as_view(), name='contact_us'),
    path('category/', AllProductsView.as_view(), name='category'),
    # path('productdetail/<slug:slug>/', ProductDetailView.as_view(), name='productdetail'),
    path('productdetail/<int:id>/', ProductDetailView.as_view(), name='productdetail'),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),name="customerorderdetail"),
    path("search/", SearchView.as_view(), name="search"),
    path("forgot-password/", ForgetPassword.as_view(), name="forgetpassword"),
    path("password-reset/<email>/<token>/",PasswordResetView.as_view(), name="passwordreset"),

]

