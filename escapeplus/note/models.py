from django.conf import settings
from django.db import models
from django.utils import timezone


class Note(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notes',
        verbose_name='보낸 사람',
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notes',
        verbose_name='받는 사람',
    )
    subject = models.CharField(max_length=120, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    is_read = models.BooleanField(default=False, verbose_name='읽음 여부')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='읽은 시간')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='보낸 시간')

    class Meta:
        db_table = 'escape_note'
        verbose_name = '쪽지'
        verbose_name_plural = '쪽지'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
        ]

    def __str__(self):
        return f'{self.sender} -> {self.recipient} | {self.subject}'

    def mark_as_read(self):
        if self.is_read:
            return

        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])

