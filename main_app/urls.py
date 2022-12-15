from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('abouts/', views.about, name='about'),
    path('films/', views.films_index, name='films_index'),
    path('films/<int:id>', views.films_detail, name='films_detail'),
    path('films/create/', views.FilmCreate.as_view(), name='create'),

    path('films/<int:pk>/update', views.FilmUpdate.as_view(), name='update'),
    path('films/<int:pk>/delete', views.FilmDelete.as_view(), name='delete'),
]
