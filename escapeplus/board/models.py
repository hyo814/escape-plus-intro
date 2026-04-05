from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='태그명')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'escape_tag'
        verbose_name = '태그'
        verbose_name_plural = '태그'

    def __str__(self):
        return self.name


class Board(models.Model):
    class Category(models.TextChoices):
        REVIEW = 'review', '리뷰'
        JOB = 'job', '구직'
        ASSIGNMENT = 'assignment', '양도'
        MAKE = 'make', '창작'
        SUGGEST = 'suggest', '질문/건의'
        TIP = 'tip', '꿀팁'
        TEAM = 'team', '대외활동'
        PLAY = 'play', '온라인'

    category = models.CharField(
        max_length=20, choices=Category.choices, verbose_name='게시판 종류'
    )
    title = models.CharField(max_length=128, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='작성자',
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='태그')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')

    class Meta:
        db_table = 'escape_board'
        verbose_name = '게시글'
        verbose_name_plural = '게시글'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
        ]

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title}'


class Comment(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='게시글',
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='작성자',
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='부모 댓글',
    )
    content = models.TextField(verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta:
        db_table = 'escape_comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['board', 'created_at']),
        ]

    def __str__(self):
        return f'{self.writer} - {self.content[:20]}'
