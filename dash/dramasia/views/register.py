from django.shortcuts import render


def register(request):
    context = {}
    return render(request, 'dramasia/register.html', context)
