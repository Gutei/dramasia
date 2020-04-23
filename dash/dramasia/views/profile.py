from django.shortcuts import render
from dramasia.models import Drama, Season, DramaSeason, SiteTemplate, ProfileUser
from django.template import Template, Context
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dateutil import parser as ps
from django.db import transaction

@login_required
def profile(request):

    profile_user = ProfileUser.objects.filter(user=request.user).first()

    if not profile_user:
        return redirect(reverse('login'))

    context = {
        'profile': profile_user,
    }

    return render(request, 'dramasia/profile.html', context)


@login_required
@transaction.atomic
def edit_profile(request, id):
    usr_prof = ProfileUser.objects.filter(id=id).first()
    if not usr_prof:
        return redirect('login')

    if request.method == 'POST':
        biodata = request.POST.get('biodata')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        photo = request.FILES.get('photo', False)
        if biodata:
            photo = None
            usr_prof.biodata = biodata
        if birth_date:
            usr_prof.birth_date = ps.parse(birth_date)
        if gender:
            usr_prof.gender = gender
        if username:
            if usr_prof.symbol < 1:
                return redirect("{}?{}".format(reverse('profile'), 'fail=5'))
            usrnm = User.objects.filter(username=username).first()
            if usrnm:
                return redirect("{}?{}".format(reverse('profile'), 'fail=4'))
            usr_prof.symbol -= 1
            usr_prof.save()

            usrnm = request.user
            usrnm.username = username
            usrnm.save()

        if photo:
            usr_prof.photo_profile = request.FILES['photo']
        try:
            usr_prof.save()
        except Exception as e:
            return redirect('profile')
    return redirect('profile')