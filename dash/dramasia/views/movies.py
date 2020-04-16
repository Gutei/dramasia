from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from dramasia.models import Drama, DramaCast, Genre


def listing_movie(request):
    movies = Drama.objects.filter(is_publish=True).order_by('-updated')
    paginator = Paginator(movies, 6)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    genre = Genre.objects.all()
    context = {
        'movies': movies_pages,
        'genres': genre,
    }
    return render(request, 'dramasia/movies/movie-list.html', context)


def griding_movie(request):
    movies = Drama.objects.filter(is_publish=True).order_by('-updated')
    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    context = {
        'movies': movies_pages,
    }
    return render(request, 'dramasia/movies/movie-grid.html', context)


def get_movie(request, pk):
    movies = Drama.objects.filter(is_publish=True).order_by('-updated')[:6]
    movie = Drama.objects.filter(id=pk).first()
    cast = DramaCast.objects.filter(drama=movie)
    context = {
        'movies': movies,
        'movie': movie,
        'cast': cast
    }
    return render(request, 'dramasia/movies/movie-view.html', context)


def post_review(request, pk):
    rate = request.POST.get('rate')
    return redirect('home')
