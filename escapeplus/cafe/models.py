from django.db import models


class Cafe(models.Model):
    name = models.CharField(max_length=128, verbose_name='카페명')
    address = models.CharField(max_length=256, verbose_name='주소')
    region = models.CharField(
        max_length=32, blank=True, verbose_name='지역',
        help_text='홍대, 강남, 건대, 신촌 등',
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='전화번호')
    theme_count = models.PositiveIntegerField(default=0, verbose_name='테마 수')
    website = models.URLField(blank=True, verbose_name='웹사이트')
    image_url = models.URLField(blank=True, verbose_name='매장 이미지')
    latitude = models.FloatField(null=True, blank=True, verbose_name='위도')
    longitude = models.FloatField(null=True, blank=True, verbose_name='경도')
    operating_hours = models.CharField(
        max_length=128, blank=True, verbose_name='영업시간',
        help_text='예: 10:00 ~ 22:00',
    )
    description = models.TextField(blank=True, verbose_name='설명')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'escape_cafe'
        verbose_name = '방탈출 카페'
        verbose_name_plural = '방탈출 카페'

    def __str__(self):
        return self.name


class Theme(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='themes',
        verbose_name='카페',
    )
    name = models.CharField(max_length=128, verbose_name='테마명')
    poster_url = models.URLField(blank=True, verbose_name='테마 포스터 이미지')
    genre = models.CharField(max_length=64, blank=True, verbose_name='장르')
    difficulty = models.PositiveSmallIntegerField(
        default=3,
        verbose_name='난이도',
        help_text='1~5 사이의 난이도',
    )
    horror_level = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='공포도',
        help_text='1~5 사이의 공포도',
    )
    activity_level = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='활동성',
        help_text='1~5 사이의 활동성',
    )
    duration_minutes = models.PositiveSmallIntegerField(
        default=60,
        verbose_name='진행 시간(분)',
    )
    min_players = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='최소 인원',
    )
    max_players = models.PositiveSmallIntegerField(
        default=6,
        verbose_name='최대 인원',
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name='가격(원)',
        help_text='1인 기준 가격',
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name='평점',
        help_text='0.0~5.0 사이의 평점',
    )
    review_count = models.PositiveIntegerField(
        default=0,
        verbose_name='리뷰 수',
    )
    clear_rate = models.FloatField(
        default=0.0,
        verbose_name='탈출률(%)',
        help_text='0~100 사이의 탈출 성공률',
    )
    booking_url = models.URLField(blank=True, verbose_name='예약 링크')
    description = models.TextField(blank=True, verbose_name='테마 설명')
    display_order = models.PositiveIntegerField(default=0, verbose_name='정렬 순서')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'escape_theme'
        verbose_name = '방탈출 테마'
        verbose_name_plural = '방탈출 테마'
        ordering = ['display_order', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['cafe', 'name'],
                name='unique_theme_name_per_cafe',
            ),
        ]

    def __str__(self):
        return f'{self.cafe.name} - {self.name}'

    @property
    def reservation_url(self):
        return self.booking_url or self.cafe.website
