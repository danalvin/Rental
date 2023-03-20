from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    path('', views.HouseListView.as_view(), name='house-list'),
    path('<int:pk>/', views.HouseDetailView.as_view(), name='house-detail'),
    path('add/', views.HouseCreateView.as_view(), name='house-create'),
    path('<int:pk>/update/', views.HouseUpdateView.as_view(), name='house-update'),
    path('<int:pk>/delete/', views.HouseDeleteView.as_view(), name='house-delete'),
    path('<int:pk>/meterreading/', views.MeterReadingCreateView.as_view(), name='meter-reading-create'),
    path('<int:pk>/meterreading/update/', views.MeterReadingUpdateView.as_view(), name='meter-reading-update'),
    path('<int:pk>/rent/update/', views.RentUpdateView.as_view(), name='rent-update'),
]
