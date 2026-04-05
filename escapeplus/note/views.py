from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


def _note_box_tabs():
    return [
        {'key': 'inbox', 'label': '받은 쪽지', 'url_name': 'note:inbox'},
        {'key': 'sent', 'label': '보낸 쪽지', 'url_name': 'note:sent'},
        {'key': 'compose', 'label': '쪽지 쓰기', 'url_name': 'note:compose'},
    ]


def _get_accessible_note(user, pk):
    note = get_object_or_404(
        Note.objects.select_related('sender', 'recipient'),
        pk=pk,
    )
    if note.sender_id != user.id and note.recipient_id != user.id:
        raise Http404('접근할 수 없는 쪽지입니다.')
    return note


@login_required
def inbox(request):
    notes = Note.objects.select_related('sender').filter(recipient=request.user)
    context = {
        'notes': notes,
        'note_box': 'inbox',
        'page_title': '받은 쪽지',
        'page_description': '다른 회원이 보낸 쪽지를 확인하고 읽음 상태를 관리할 수 있습니다.',
        'tabs': _note_box_tabs(),
    }
    return render(request, 'note/list.html', context)


@login_required
def sent(request):
    notes = Note.objects.select_related('recipient').filter(sender=request.user)
    context = {
        'notes': notes,
        'note_box': 'sent',
        'page_title': '보낸 쪽지',
        'page_description': '내가 보낸 쪽지와 상대방의 읽음 상태를 확인할 수 있습니다.',
        'tabs': _note_box_tabs(),
    }
    return render(request, 'note/list.html', context)


@login_required
def compose(request):
    initial = {}
    recipient_id = request.GET.get('to')
    subject = request.GET.get('subject')

    if recipient_id:
        recipient = get_user_model().objects.filter(pk=recipient_id).exclude(pk=request.user.pk).first()
        if recipient:
            initial['recipient'] = recipient

    if subject:
        initial['subject'] = subject

    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.sender = request.user
            note.save()
            messages.success(request, '쪽지를 보냈습니다.')
            return redirect('note:detail', pk=note.pk)
    else:
        form = NoteForm(user=request.user, initial=initial)

    context = {
        'form': form,
        'note_box': 'compose',
        'tabs': _note_box_tabs(),
    }
    return render(request, 'note/compose.html', context)


@login_required
def detail(request, pk):
    note = _get_accessible_note(request.user, pk)

    if note.recipient_id == request.user.id:
        note.mark_as_read()

    is_inbox_view = note.recipient_id == request.user.id
    other_user = note.sender if is_inbox_view else note.recipient
    subject_prefix = '[답장] '
    reply_subject = note.subject
    if not note.subject.startswith(subject_prefix):
        reply_subject = f'{subject_prefix}{note.subject}'

    context = {
        'note': note,
        'other_user': other_user,
        'reply_subject': reply_subject,
        'note_box': 'inbox' if is_inbox_view else 'sent',
        'tabs': _note_box_tabs(),
    }
    return render(request, 'note/detail.html', context)

