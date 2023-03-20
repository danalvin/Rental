from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    path('', views.house_list, name='house_list'),
    path('<int:pk>/', views.house_detail, name='house_detail'),
    path('<int:pk>/update/', views.HouseUpdateView.as_view(), name='house_update'),
    path('meter/<int:pk>/update/', views.MeterReadingUpdateView.as_view(), name='meter_update'),
]
