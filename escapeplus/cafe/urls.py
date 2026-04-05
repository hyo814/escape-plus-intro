from django.urls import path
from . import views

app_name = 'cafe'

urlpatterns = [
    path('', views.cafe_list, name='cafe_list'),
    path('<int:pk>/', views.cafe_detail, name='cafe_detail'),
]
