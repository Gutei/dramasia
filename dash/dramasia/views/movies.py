from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from dramasia.models import Drama, DramaCast, Genre, DramaGenre
from django.http import Http404


def listing_movie(request):
    movies = Drama.objects.filter(is_publish=True).order_by('-title')

    if request.GET.get('country') and request.GET.get('country') != 'Semua':
        if not request.GET.get('genre') or request.GET.get('genre') == 'Semua':
            movies = Drama.objects.filter(is_publish=True, country=request.GET.get('country')).order_by('-title')
        else:
            movies = DramaGenre.objects.filter(genre__genre=request.GET.get('genre'), drama__is_publish=True,
                                               drama__country=request.GET.get('country')).order_by('-title')

    paginator = Paginator(movies, 6)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    genre = Genre.objects.all()

    country = Drama.objects.values('country').distinct()

    context = {
        'movies': movies_pages,
        'genres': genre,
        'countries': country,
    }
    return render(request, 'dramasia/movies/movie-list.html', context)


def griding_movie(request):
    movies = Drama.objects.filter(is_publish=True).order_by('-title')

    if request.GET.get('country') and request.GET.get('country') != 'Semua':
        if not request.GET.get('genre') or request.GET.get('genre') == 'Semua':
            movies = Drama.objects.filter(is_publish=True, country=request.GET.get('country')).order_by('-title')
        else:
            movies = DramaGenre.objects.filter(genre__genre=request.GET.get('genre'), drama__is_publish=True, drama__country=request.GET.get('country')).order_by('-title')

    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    context = {
        'movies': movies_pages,
    }
    return render(request, 'dramasia/movies/movie-grid.html', context)


def get_movie(request, pk):
    movies = Drama.objects.filter(is_publish=True).order_by('-updated')[:6]
    movie = Drama.objects.filter(slug=pk).first()

    if not movie:
        raise Http404("Not Found.")

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
