from django.shortcuts import render


def listing_movie(request):
    context = {}
    return render(request, 'dramasia/movies/movie-list.html', context)


def griding_movie(request):
    context = {}
    return render(request, 'dramasia/movies/movie-grid.html', context)
