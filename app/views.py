from django.shortcuts import render
from django.core.management import call_command


def home(request):
    return render(request, 'app/home.html')
