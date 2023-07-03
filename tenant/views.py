from django.views.generic import CreateView, TemplateView, View
from .forms import TenantSignUpForm
from django.shortcuts import render
from .models import tenant

class TenantSignUpView(CreateView):
    model = tenant
    form_class = TenantSignUpForm
    template_name = 'tenantapp/signup.html'
    success_url = '/signup/success/'

class SignUpSuccessView(TemplateView):
    template_name = 'tenantapp/signup_success.html'

class SignupView(View):
    def get(self, request):
        return render(request, 'home/home.html')