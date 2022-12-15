from django.db import models
from django.urls import reverse

# Create your models here.
CHOICE = ('1', '2', '3', '4', '5')


class Film(models.Model):
    name = models.CharField(max_length=100)
    year_released = models.IntegerField()
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})


class Review(models.Model):
    rating = models.CharField(
        max_length=1)
    description = models.TextField(max_length=250)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def _str__(self):
        return f"{self.film} has a rating of {self.rating} with the description {self.description}"
