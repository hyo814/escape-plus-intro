from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteViewTests(TestCase):
    def setUp(self):
        self.sender = get_user_model().objects.create_user(
            username='sender',
            password='testpass123',
            nickname='보낸사람',
        )
        self.recipient = get_user_model().objects.create_user(
            username='recipient',
            password='testpass123',
            nickname='받는사람',
        )

    def test_inbox_detail_marks_note_as_read(self):
        note = Note.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject='안녕하세요',
            content='쪽지 테스트입니다.',
        )

        self.client.login(username='recipient', password='testpass123')
        response = self.client.get(reverse('note:detail', args=[note.id]))

        self.assertEqual(response.status_code, 200)
        note.refresh_from_db()
        self.assertTrue(note.is_read)

    def test_compose_creates_note(self):
        self.client.login(username='sender', password='testpass123')
        response = self.client.post(
            reverse('note:compose'),
            data={
                'recipient': self.recipient.id,
                'subject': '문의드립니다',
                'content': '간단한 쪽지 기능 테스트입니다.',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.first()
        self.assertEqual(note.sender, self.sender)
        self.assertEqual(note.recipient, self.recipient)

