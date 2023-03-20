from django.urls import path
from .views import (
    OccupationListView,
    OccupationCreateView,
    OccupationUpdateView,
    PaymentCreateView,
    PaymentUpdateView
)

app_name = 'occupations'

urlpatterns = [
    path('', OccupationListView.as_view(), name='occupation_list'),
    path('create/', OccupationCreateView.as_view(), name='occupation_create'),
    path('<int:pk>/update/', OccupationUpdateView.as_view(), name='occupation_update'),
    path('<int:pk>/payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('<int:pk>/payment/update/<int:payment_id>/', PaymentUpdateView.as_view(), name='payment_update'),
]
