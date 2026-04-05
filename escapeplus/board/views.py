from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import Http404

from .models import Board, Comment, Tag
from .forms import BoardForm, CommentForm


def home(request):
    from cafe.models import Cafe
    cafes = Cafe.objects.all()
    cafe_count = cafes.count()
    theme_count = cafes.aggregate(total=Sum('theme_count'))['total'] or 0
    return render(request, 'home.html', {
        'cafe_count': cafe_count,
        'theme_count': theme_count,
    })


def board_list(request, category):
    if category not in Board.Category.values:
        raise Http404
    boards = Board.objects.filter(category=category)
    page = int(request.GET.get('p', 1))
    paginator = Paginator(boards, 10)
    page_obj = paginator.get_page(page)
    numbered_boards = []
    for index, board in enumerate(page_obj.object_list, start=page_obj.start_index()):
        board.list_number = paginator.count - index + 1
        numbered_boards.append(board)
    context = {
        'boards': numbered_boards,
        'page_obj': page_obj,
        'category': category,
        'category_display': Board.Category(category).label,
    }
    return render(request, 'board/board_list.html', context)


def board_detail(request, category, pk):
    board = get_object_or_404(Board, pk=pk, category=category)
    if request.method == 'GET':
        board.view_count += 1
        board.save(update_fields=['view_count'])
    comments = board.comments.select_related('writer', 'parent').prefetch_related('replies__writer')
    root_comments = comments.filter(parent__isnull=True)
    return render(request, 'board/board_detail.html', {
        'board': board,
        'category': category,
        'comment_form': CommentForm(),
        'comments': root_comments,
    })


@login_required
def board_write(request, category):
    if category not in Board.Category.values:
        raise Http404
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.writer = request.user
            board.category = category
            board.save()
            tag_string = form.cleaned_data.get('tag_string', '')
            for tag_name in tag_string.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    board.tags.add(tag)
            return redirect('board:board_list', category=category)
    else:
        form = BoardForm()
    return render(request, 'board/board_write.html', {
        'form': form,
        'category': category,
        'category_display': Board.Category(category).label,
    })


@login_required
def board_delete(request, category, pk):
    board = get_object_or_404(Board, pk=pk, category=category)
    if board.writer != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        board.delete()
        return redirect('board:board_list', category=category)
    return redirect('board:board_detail', category=category, pk=pk)


@login_required
def comment_create(request, category, pk):
    board = get_object_or_404(Board, pk=pk, category=category)
    if request.method != 'POST':
        return redirect('board:board_detail', category=category, pk=pk)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.board = board
        comment.writer = request.user
        parent_id = form.cleaned_data.get('parent_id')
        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id, board=board)
            if parent.parent_id:
                parent = parent.parent
            comment.parent = parent
        comment.save()

    return redirect('board:board_detail', category=category, pk=pk)
