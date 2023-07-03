from django.urls import path
from .views import TenantSignUpView, SignUpSuccessView,SignupView

app_name = 'tenant'

urlpatterns = [
    path('signup/', TenantSignUpView.as_view(), name='signup'),
    path('signup/success/', SignUpSuccessView.as_view(), name='signup_success'),
    path('', SignupView.as_view(), name='home'),
]