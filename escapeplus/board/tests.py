from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Board, Comment


class BoardCommentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester',
            password='pass1234',
            nickname='테스터',
        )
        self.board = Board.objects.create(
            category=Board.Category.REVIEW,
            title='테스트 게시글',
            contents='본문',
            writer=self.user,
        )

    def test_board_list_shows_sequence_number_not_database_id(self):
        response = self.client.get(reverse('board:board_list', args=[Board.Category.REVIEW]))

        self.assertContains(response, '<td>1</td>', html=True)

    def test_board_list_numbers_descend_from_total_count(self):
        for index in range(2, 12):
            Board.objects.create(
                category=Board.Category.REVIEW,
                title=f'게시글 {index}',
                contents='본문',
                writer=self.user,
            )

        response = self.client.get(reverse('board:board_list', args=[Board.Category.REVIEW]))

        self.assertContains(response, '<td>11</td>', html=True)
        self.assertContains(response, '<td>2</td>', html=True)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='tester', password='pass1234')

        response = self.client.post(
            reverse('board:comment_create', args=[Board.Category.REVIEW, self.board.pk]),
            {'content': '첫 댓글입니다.'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(board=self.board, content='첫 댓글입니다.').exists())

    def test_logged_in_user_can_create_reply(self):
        parent = Comment.objects.create(
            board=self.board,
            writer=self.user,
            content='부모 댓글',
        )
        self.client.login(username='tester', password='pass1234')

        response = self.client.post(
            reverse('board:comment_create', args=[Board.Category.REVIEW, self.board.pk]),
            {'content': '대댓글', 'parent_id': parent.pk},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(parent=parent, content='대댓글').exists())

    def test_board_detail_renders_comment_and_reply(self):
        parent = Comment.objects.create(
            board=self.board,
            writer=self.user,
            content='부모 댓글',
        )
        Comment.objects.create(
            board=self.board,
            writer=self.user,
            parent=parent,
            content='대댓글',
        )

        response = self.client.get(reverse('board:board_detail', args=[Board.Category.REVIEW, self.board.pk]))

        self.assertContains(response, '부모 댓글')
        self.assertContains(response, '대댓글')
