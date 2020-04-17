from django.shortcuts import render
from dramasia.models import Drama, Season, DramaSeason

def home(request):
    # this_season = Drama.objects.filter(is_publish=True).order_by('-updated')[:8]
    season = Season.objects.filter(is_season=True).first()
    drama_season = DramaSeason.objects.filter(season=season).order_by('-updated')[:8]
    ds_list = []
    for ds in drama_season:
        ds_list.append(ds.drama)

    drama = Drama.objects.filter(is_publish=True).order_by('-updated')[:6]
    context = {
        'this_season': ds_list,
        'drama': drama
    }
    return render(request, 'dramasia/home.html', context)