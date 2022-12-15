from django.shortcuts import render
from .models import Film
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, 'about.html')


def films_index(request):
    films = Film.objects.all()
    return render(request, 'films/index.html/', {'film': films})


def films_detail(request, film_id):
    film = Film.objects.get(film_id)
    return render(request, 'films/details/', {'film': film})


class FilmCreate(CreateView):
    model = Film
    fields = '__all__'


class FilmUpdate(UpdateView):
    model = Film
    fields = ['year_released', 'description']


class FilmDelete(DeleteView):
    model = Film
    success_url = '/films/'
