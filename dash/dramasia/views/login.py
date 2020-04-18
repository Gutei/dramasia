from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def login(request):
    context = {}

    return render(request, 'dramasia/login.html', context)



def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return redirect(reverse('home'))
        else:
            return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))
