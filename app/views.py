from django.shortcuts import render
from django.core.management import call_command

from app.forms import HomeForm


def home(request):
    c = dict()
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            pass
    c['form'] = HomeForm()
    return render(request, 'app/home.html', c)
