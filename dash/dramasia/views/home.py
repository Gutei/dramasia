from django.shortcuts import render
from dramasia.models import Drama, Season

def home(request):
    this_season = Drama.object.all().order_by('-updated')[:4]
    drama = Drama.object.all().order_by('-updated')[:8]
    context = {
        'this_season': this_season,
        'drama': drama
    }
    return render(request, 'dramasia/home.html', context)