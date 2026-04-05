from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('<str:category>/', views.board_list, name='board_list'),
    path('<str:category>/write/', views.board_write, name='board_write'),
    path('<str:category>/<int:pk>/', views.board_detail, name='board_detail'),
    path('<str:category>/<int:pk>/comments/', views.comment_create, name='comment_create'),
    path('<str:category>/<int:pk>/delete/', views.board_delete, name='board_delete'),
]
