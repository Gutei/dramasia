from django.core.paginator import Paginator
from django.shortcuts import render
from dramasia.models import Drama


def listing_movie(request):
    movies = Drama.objects.filter(type=2).order_by('-updated')
    paginator = Paginator(movies, 6)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    context = {
        'movies': movies_pages,
    }
    return render(request, 'dramasia/movies/movie-list.html', context)


def griding_movie(request):
    movies = Drama.objects.filter(type=2).order_by('-updated')
    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    context = {
        'movies': movies_pages,
    }
    return render(request, 'dramasia/movies/movie-grid.html', context)


def get_movie(request, pk):
    movie = Drama.objects.filter(id=pk).first()
    context = {
        'movie': movie
    }
    return render(request, 'dramasia/movies/movie-view.html', context)
