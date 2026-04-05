from django.core.management.base import BaseCommand

from cafe.models import Cafe, Theme
from cafe.seed_data import VERIFIED_CAFE_THEME_SEED


class Command(BaseCommand):
    help = 'Seed verified cafe theme data into the local database.'

    def handle(self, *args, **options):
        updated_cafes = 0
        created_themes = 0

        for cafe_name, payload in VERIFIED_CAFE_THEME_SEED.items():
            cafe = Cafe.objects.filter(name=cafe_name).first()
            if not cafe:
                self.stdout.write(self.style.WARNING(f'Cafe not found: {cafe_name}'))
                continue

            website = payload.get('website', '').strip()
            if website and cafe.website != website:
                cafe.website = website
                cafe.save(update_fields=['website'])

            for order, theme_data in enumerate(payload.get('themes', []), start=1):
                defaults = {
                    'genre': theme_data.get('genre', ''),
                    'difficulty': theme_data.get('difficulty', 3),
                    'duration_minutes': theme_data.get('duration_minutes', 60),
                    'booking_url': theme_data.get('booking_url', website),
                    'description': theme_data.get('description', ''),
                    'display_order': order,
                }
                theme, created = Theme.objects.update_or_create(
                    cafe=cafe,
                    name=theme_data['name'],
                    defaults=defaults,
                )
                if created:
                    created_themes += 1
                elif theme.display_order != order:
                    theme.display_order = order
                    theme.save(update_fields=['display_order'])

            updated_cafes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Seed sync complete: {updated_cafes} cafes updated, {created_themes} themes created.'
            )
        )
