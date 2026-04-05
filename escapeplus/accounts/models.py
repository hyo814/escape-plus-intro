from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    kakao_id = models.BigIntegerField(
        unique=True, null=True, blank=True, verbose_name='카카오 ID'
    )
    nickname = models.CharField(
        max_length=64, blank=True, verbose_name='닉네임'
    )
    profile_image = models.URLField(
        blank=True, verbose_name='프로필 이미지 URL'
    )

    class Meta:
        db_table = 'escape_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def __str__(self):
        return self.nickname or self.username
