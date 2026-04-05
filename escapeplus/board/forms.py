from django import forms
from .models import Board, Comment


class BoardForm(forms.ModelForm):
    tag_string = forms.CharField(max_length=256, required=False, label='태그')

    class Meta:
        model = Board
        fields = ['title', 'contents']


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': '댓글을 입력하세요',
            }),
        }
        labels = {
            'content': '댓글',
        }
