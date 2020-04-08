"""dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from dramasia import views

admin.site.site_header = 'dramAsia'

urlpatterns = [
                  url(r'^jet', include('jet.urls', 'jet')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^teh-olong/', admin.site.urls),
                  url(r'^$', views.home, name='home'),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^movies-grid/$', views.griding_movie, name='movies_grid'),
                  url(r'^movies-list/$', views.listing_movie, name='movies_list'),
                  url(r'^movie/(?P<pk>[^/]+)/$', views.get_movie, name='get_movie'),
                  url(r'^post-review-movie/(?P<pk>[^/]+)/$', views.post_review, name='post_review_movie'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
