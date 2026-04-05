from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('compose/', views.compose, name='compose'),
    path('<int:pk>/', views.detail, name='detail'),
]

