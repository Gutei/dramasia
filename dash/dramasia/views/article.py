from django.shortcuts import render
from dramasia.models import Drama, Season, DramaSeason, Article
from django.http import Http404
from django.core.paginator import Paginator

def get_article(request, slug):
    article = Article.objects.filter(is_publish=True, slug=slug).first()

    if not article:
        raise Http404("Not Found.")

    context = {
        'article': article,
    }
    return render(request, 'dramasia/article/get_article_2.html', context)


def list_article(request):
    articles = Article.objects.filter(is_publish=True)

    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    article_pages = paginator.get_page(page)

    context = {
        'articles': article_pages,
    }
    return render(request, 'dramasia/article/article-list.html', context)