from django.shortcuts import render

from django.contrib.auth import authenticate, login as do_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def login(request):
    context = {}

    return render(request, 'dramasia/login.html', context)


def auth_login(request):
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
      if user.is_active:
        do_login(request, user)
        return redirect(reverse('home'))
      else:
        return redirect('{}?{}'.format(reverse('login'), 'failed=1'))
    else:
      # print("Someone tried to login and failed.")
      # print("They used username: {} and password: {}".format(username, password))
      return redirect('{}?{}'.format(reverse('login'), 'failed=2'))

  return redirect('{}?{}'.format(reverse('login'), 'failed=3'))