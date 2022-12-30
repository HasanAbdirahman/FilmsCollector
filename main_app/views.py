from django.shortcuts import render, redirect
from .models import Film, Cast, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ReviewForm
from django.views.generic import ListView, DetailView
# image upload using S3 AWS
import boto3
import uuid
# auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'hasan-film-collector'

# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, 'about.html')


@login_required
def films_index(request):
    films = Film.objects.filter(user=request.user)
    print(films)
    return render(request, 'films/index.html', {'films': films})


@login_required
def films_detail(request, id):
    film = Film.objects.get(id=id)
    # gives us the form columns that FormModel is going to use to create the model
    review_form = ReviewForm()
    print(film.review_set.all())
    return render(request, 'films/details.html', {'film': film, 'review_form': review_form})


@login_required
def add_review(request, film_id):
    # create the ModelForm using the data in request.POST
    form = ReviewForm(request.POST)

    # VALIDATING the form
    if form.is_valid():
        print('hello')
        # don't save the form to the db until it
        # has the film_id assigned
        new_review = form.save(commit=False)
        new_review.film_id = film_id
        new_review.save()
    return redirect('detail', id=film_id)


class FilmCreate(LoginRequiredMixin, CreateView):
    model = Film
    fields = ['name', 'year_released', 'description']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the film
    # Let the CreateView do its job as usual
    # Accordingly, after updating the form to include the user, we're calling super().form_valid(form) to let the CreateView do its usual job of creating the model in the database and redirecting.
        return super().form_valid(form)


class FilmUpdate(LoginRequiredMixin, UpdateView):
    model = Film
    fields = ['year_released', 'description']


class FilmDelete(LoginRequiredMixin, DeleteView):
    model = Film
    success_url = '/films/'


# CAST Classes
class ListCast(LoginRequiredMixin, ListView):
    model = Cast


class CastDetails(LoginRequiredMixin, DetailView):
    model = Cast


class CastCreate(LoginRequiredMixin, CreateView):
    model = Cast
    fields = "__all__"
    success_url = '/casts/'


class CastUpdate(LoginRequiredMixin, UpdateView):
    model = Cast
    fields = ['name', 'age']
    success_url = '/casts/'


class CastDelete(LoginRequiredMixin, DeleteView):
    model = Cast
    success_url = '/casts/'


@login_required
def add_photo(request, film_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        # try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        # build the full url string
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # we can assign to film id or film (if you have a cat object)
        photo = Photo(url=url, id=film_id)
        print(photo)
        photo.save()
        # except:
        #     print('An error occurred uploading file to S3')
    return redirect('detail', id=film_id)


# def signup(request):
#     error_message = ''
#     if request.method == 'POST':
#         # This is how to create a 'user' form object
#         # that includes the data from the browser
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#           # This will add the user to the database
#             user = form.save()
#             # This is how we log a user in via code
#             login(request, user)
#             return redirect('films/index')
#         else:
#             error_message = 'Invalid sign up - try again'
#     # A bad POST or a GET request, so render signup.html with an empty form
#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)

def signup(request):
    message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'message': message})
