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

from rest_framework import routers
from dramasia.api.viewsets.drama import DramaViewSet, GenreViewSet
from dramasia.api.viewsets.cast import CastViewSet
from dramasia.api.viewsets.auth import UserViewSet
from dramasia.api.viewsets.user import UpdateUserViewSet, DjangoUserViewSet, RegisterUserViewSet
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='dramAsia API')

admin.site.site_header = 'dramAsia'

router = routers.DefaultRouter()
router.register(r'drama', DramaViewSet)
router.register(r'cast', CastViewSet)
router.register(r'auth', UserViewSet)
router.register(r'update-auth', UpdateUserViewSet)
router.register(r'user/profile', DjangoUserViewSet)
router.register(r'user/register', RegisterUserViewSet)
router.register(r'genre', GenreViewSet)

drama = routers.SimpleRouter()
drama.register(r'', DramaViewSet)

cast = routers.SimpleRouter()
cast.register(r'', CastViewSet)

auth = routers.SimpleRouter()
auth.register(r'', UserViewSet)

update_user = routers.SimpleRouter()
update_user.register(r'', UpdateUserViewSet)

urlpatterns = [
                  url(r'^jet', include('jet.urls', 'jet')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^teh-olong/', admin.site.urls),
                  url(r'^$', views.home, name='home'),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^movies-grid/$', views.griding_movie, name='movies_grid'),
                  url(r'^content-list/$', views.listing_movie, name='movies_list'),
                  url(r'^content/(?P<pk>[^/]+)/$', views.get_movie, name='get_movie'),
                  url(r'^cast-list/$', views.listing_cast, name='casts_list'),
                  url(r'^post-review-movie/(?P<pk>[^/]+)/$', views.post_review, name='post_review_movie'),
                  url(r'^developer/stellarium', schema_view),
                  url(r'^nebula/v1/', include(router.urls)),
                  url(r'^api-auth/', include('rest_framework.urls',  namespace='rest_framework')),


              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
