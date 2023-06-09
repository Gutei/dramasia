import random
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from dramasia.models import Drama, DramaCast, Genre, DramaGenre, SiteTemplate
from django.http import Http404
from django.template import Template, Context
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound


def listing_movie(request):
    movies = Drama.objects.filter(is_publish=True).order_by('title')
    second_head = "Semua Genre di Semua Negara"
    if request.GET.get('country') and request.GET.get('country') != 'Semua':
        if not request.GET.get('genre') or request.GET.get('genre') == 'Semua':
            second_head = "Semua Genre di Movie/Series {}".format(request.GET.get('country'))
            movies = Drama.objects.filter(is_publish=True, country=request.GET.get('country')).order_by('title')
        else:
            second_head = "Genre {} di Movie/Series {}".format(request.GET.get('genre'), request.GET.get('country'))
            movies = DramaGenre.objects.filter(genre__genre=request.GET.get('genre'), drama__is_publish=True,
                                               drama__country=request.GET.get('country')).order_by('drama__title')

            lm = []
            for m in movies:
                lm.append(m.drama)

            movies = lm

    if request.GET.get('q') and request.GET.get('q') != '':
        second_head = "Hasil pencarian dengan keyword {}".format(request.GET.get('q'))
        movies = Drama.objects.filter(is_publish=True, title__icontains=request.GET.get('q')).order_by('title')

    paginator = Paginator(movies, 6)
    page = request.GET.get('page')
    movies_pages = paginator.get_page(page)
    genre = Genre.objects.all().order_by('genre')

    country = Drama.objects.values('country').distinct()

    context = {
        'movies': movies_pages,
        'genres': genre,
        'countries': country,
        'second_head': second_head,
        'request': {
            'user': request.user,
        }
    }

    template = SiteTemplate.objects.filter(code='MoviesSeriesList', is_active=True).first()
    if template:
        t = Template(template.content)
        context = Context(context)
        return HttpResponse(t.render(context))

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
        'request': {
            'user': request.user,
        }
    }
    return render(request, 'dramasia/movies/movie-grid.html', context)


def get_movie(request, pk):
    movies = Drama.objects.filter(is_publish=True).order_by('-updated')[:6]
    movie = Drama.objects.filter(slug=pk).first()

    drama_genre = DramaGenre.objects.filter(drama=movie)
    genres = []
    for dg in drama_genre:
        genres.append(dg.genre.genre)

    movies = DramaGenre.objects.filter(genre__genre__in=genres, drama__is_publish=True).exclude(drama=movie).distinct('drama')

    lm = []
    for m in movies:
        lm.append(m.drama)

    movies = lm

    if not movie:
        raise Http404("Not Found.")

    if len(movies) > 10:
        ses_anime_random_sample = 10
        shuffle_ses_anime = random.sample(set(movies), ses_anime_random_sample)
    else:
        shuffle_ses_anime = movies

    cast = DramaCast.objects.filter(drama=movie)
    context = {
        'movies': shuffle_ses_anime,
        'movie': movie,
        'cast': cast,
        'genres': genres,
        'request': {
            'user': request.user,
        }
    }

    template = SiteTemplate.objects.filter(code='MoviesSeriesDetail', is_active=True).first()
    if template:
        t = Template(template.content)
        context = Context(context)
        return HttpResponse(t.render(context))

    return render(request, 'dramasia/movies/movie-view.html', context)


def post_review(request, pk):
    rate = request.POST.get('rate')
    return redirect('home')
