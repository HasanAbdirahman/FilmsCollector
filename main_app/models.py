from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
CHOICE = (
    ('1', 'one'),
    ('2', 'two'),
    ('3', 'three'),
    ('4', 'four'),
    ('5', 'five')
)


class Cast(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cast_detail', kwargs={'pk': self.id})


class Film(models.Model):
    name = models.CharField(max_length=100)
    year_released = models.IntegerField()
    description = models.CharField(max_length=250)
    cast = models.ManyToManyField(Cast)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id': self.id})


class Review(models.Model):
    date = models.DateField()
    rating = models.CharField(
        max_length=1, choices=CHOICE, default=CHOICE[4][0])

    description = models.TextField(max_length=250)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def _str__(self):
        return f"{self.film} has a rating of {self.get_rating_display()} with the description {self.description}"

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    photo = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for film_id: {self.photo_id} @{self.url}"
