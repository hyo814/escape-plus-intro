from django.contrib import admin
from .models import Cafe, Theme


class ThemeInline(admin.TabularInline):
    model = Theme
    extra = 1
    fields = (
        'name', 'poster_url', 'genre', 'difficulty', 'horror_level', 'activity_level',
        'duration_minutes', 'min_players', 'max_players', 'price',
        'rating', 'review_count', 'clear_rate', 'booking_url', 'display_order',
    )


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'address', 'theme_count', 'phone', 'operating_hours')
    list_filter = ('region',)
    search_fields = ('name', 'address', 'region')
    inlines = [ThemeInline]


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'cafe', 'genre', 'difficulty', 'horror_level', 'activity_level',
        'min_players', 'max_players', 'price', 'rating', 'review_count', 'clear_rate',
    )
    list_filter = ('genre', 'difficulty', 'horror_level', 'activity_level', 'cafe')
    search_fields = ('name', 'cafe__name')
