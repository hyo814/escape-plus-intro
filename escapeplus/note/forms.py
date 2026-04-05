from django import forms
from django.contrib.auth import get_user_model

from .models import Note


class RecipientChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nickname or obj.username


class NoteForm(forms.ModelForm):
    recipient = RecipientChoiceField(
        queryset=get_user_model().objects.none(),
        empty_label='받는 사람을 선택하세요',
        label='받는 사람',
    )

    class Meta:
        model = Note
        fields = ['recipient', 'subject', 'content']
        widgets = {
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '쪽지 제목을 입력하세요',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 8,
                    'placeholder': '전달할 내용을 입력하세요',
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        user_queryset = get_user_model().objects.all().order_by('nickname', 'username')

        if user is not None:
            user_queryset = user_queryset.exclude(pk=user.pk)

        self.fields['recipient'].queryset = user_queryset
        self.fields['recipient'].widget.attrs.update({'class': 'form-select'})

