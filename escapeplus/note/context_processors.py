from .models import Note


def unread_note_count(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {'unread_note_count': 0}

    return {
        'unread_note_count': Note.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count()
    }

