from django.contrib import admin
from django.urls import path, include
from board.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('board/', include('board.urls')),
    path('cafe/', include('cafe.urls')),
    path('maps/', include('maps.urls')),
    path('notes/', include('note.urls')),
    path('', home, name='home'),
]
