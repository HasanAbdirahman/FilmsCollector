from django.contrib import admin
from .models import Film, Review, Cast, Photo
# Register your models here.
admin.site.register(Film)
admin.site.register(Review)
admin.site.register(Cast)
admin.site.register(Photo)
