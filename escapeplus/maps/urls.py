from django.urls import path
from . import views

app_name = 'maps'

urlpatterns = [
    path('search/', views.map_search, name='map_search'),
    path('best/', views.map_best, name='map_best'),
]
