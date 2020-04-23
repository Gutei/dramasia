from django.shortcuts import render
from dramasia.models import Drama, Season, DramaSeason, SiteTemplate
from django.template import Template, Context
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound

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
        'drama': drama,
        'request': {
            'user': request.user,
        }
    }

    template = SiteTemplate.objects.filter(code='Home', is_active=True).first()
    if template:
        t = Template(template.content)
        context = Context(context)
        return HttpResponse(t.render(context))

    return render(request, 'dramasia/home.html', context)


def disclaimer(request):
    context = {
        'request': {
            'user': request.user,
        }
    }

    template = SiteTemplate.objects.filter(code='Disclaimer', is_active=True).first()
    if template:
        t = Template(template.content)
        context = Context(context)
        return HttpResponse(t.render(context))

    return render(request, 'dramasia/disclaimer.html', context)

def privacy(request):
    context = {
        'request': {
            'user': request.user,
        }
    }

    template = SiteTemplate.objects.filter(code='Privacy', is_active=True).first()
    if template:
        t = Template(template.content)
        context = Context(context)
        return HttpResponse(t.render(context))

    return render(request, 'dramasia/privacy-policy.html', context)


def get_sitemaps(request):
    template_name = 'dramasia/sitemap.xml'
    return render(request, template_name, content_type="text/xml")

def robots_txt(request):
    context = {}

    return render(request, 'dramasia/robots.txt', context, content_type="text/plain")
