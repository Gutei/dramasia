from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from dramasia.models import Drama, DramaCast, Genre, Cast, DramaCast


def listing_cast(request):
    casts = Cast.objects.all().order_by('-updated')
    paginator = Paginator(casts, 20)
    page = request.GET.get('page')
    casts_pages = paginator.get_page(page)

    context = {
        'casts': casts_pages,
    }
    return render(request, 'dramasia/casts/cast-list.html', context)
