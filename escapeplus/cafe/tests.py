from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

from .models import Cafe, Theme


class CafeViewTests(TestCase):
    def test_cafe_detail_shows_theme_and_booking_link(self):
        cafe = Cafe.objects.create(
            name='테스트 카페',
            address='서울 어딘가',
            theme_count=1,
            website='https://example.com/cafe',
        )
        Theme.objects.create(
            cafe=cafe,
            name='테스트 테마',
            genre='추리',
            difficulty=4,
            duration_minutes=75,
            booking_url='https://example.com/book/theme',
        )

        response = self.client.get(reverse('cafe:cafe_detail', args=[cafe.pk]))

        self.assertContains(response, '테스트 테마')
        self.assertContains(response, 'https://example.com/book/theme')
        self.assertContains(response, '예약하기')

    def test_cafe_detail_uses_cafe_website_when_theme_booking_link_missing(self):
        cafe = Cafe.objects.create(
            name='폴백 카페',
            address='서울 어딘가',
            theme_count=1,
            website='https://example.com/cafe-home',
        )
        Theme.objects.create(
            cafe=cafe,
            name='폴백 테마',
            genre='공포',
            difficulty=3,
            duration_minutes=60,
        )

        response = self.client.get(reverse('cafe:cafe_detail', args=[cafe.pk]))

        self.assertContains(response, '폴백 테마')
        self.assertContains(response, 'https://example.com/cafe-home')

    def test_cafe_list_shows_registered_theme_names(self):
        cafe = Cafe.objects.create(
            name='목록 카페',
            address='부산 어딘가',
            theme_count=2,
        )
        Theme.objects.create(cafe=cafe, name='첫 번째 테마')
        Theme.objects.create(cafe=cafe, name='두 번째 테마')

        response = self.client.get(reverse('cafe:cafe_list'))

        self.assertContains(response, '첫 번째 테마')
        self.assertContains(response, '두 번째 테마')

    def test_cafe_list_shows_reservation_site_button_when_website_exists(self):
        cafe = Cafe.objects.create(
            name='예약 카페',
            address='서울 어딘가',
            theme_count=1,
            website='https://example.com/reserve',
        )
        Theme.objects.create(cafe=cafe, name='예약 테마')

        response = self.client.get(reverse('cafe:cafe_list'))

        self.assertContains(response, '예약 사이트')
        self.assertContains(response, 'https://example.com/reserve')


class CafeSeedCommandTests(TestCase):
    def test_sync_cafe_theme_seed_populates_verified_data(self):
        Cafe.objects.create(
            name='코드케이 홍대점',
            address='서울 마포구 어딘가',
            theme_count=4,
        )

        call_command('sync_cafe_theme_seed')

        cafe = Cafe.objects.get(name='코드케이 홍대점')
        self.assertEqual(cafe.website, 'https://www.code-k.co.kr/')
        self.assertTrue(cafe.themes.filter(name='감옥탈출').exists())
        self.assertTrue(cafe.themes.filter(name='미스터리 거울의 방').exists())
