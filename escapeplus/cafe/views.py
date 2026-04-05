from django.shortcuts import render, get_object_or_404
from .models import Cafe


def cafe_list(request):
    cafes = Cafe.objects.prefetch_related('themes').all().order_by('name')
    return render(request, 'cafe/cafe_list.html', {'cafes': cafes})


def cafe_detail(request, pk):
    cafe = get_object_or_404(Cafe.objects.prefetch_related('themes'), pk=pk)
    return render(request, 'cafe/cafe_detail.html', {'cafe': cafe})
