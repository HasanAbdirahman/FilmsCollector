from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('abouts/', views.about, name='about'),
    path('films/', views.films_index, name='films_index'),
    path('films/<int:id>', views.films_detail, name='detail'),
    path('films/create/', views.FilmCreate.as_view(), name='create'),

    path('films/<int:pk>/update/', views.FilmUpdate.as_view(), name='update'),
    path('films/<int:pk>/delete/', views.FilmDelete.as_view(), name='delete'),

    path('films/<int:film_id>/add_review/',
         views.add_review, name='add_review'),


    # cast route
    path('casts/', views.ListCast.as_view(), name='casts_index'),
    path('casts/<int:pk>/', views.CastDetails.as_view(), name='cast_detail'),
    path('casts/create/', views.CastCreate.as_view(), name='cast_create'),

    path('casts/<int:pk>/update/', views.CastUpdate.as_view(), name='cast_update'),
    path('casts/<int:pk>/delete/', views.CastDelete.as_view(), name='cast_delete'),


    path('films/<int:film_id>/add_photo/', views.add_photo, name='add_photo'),


    path('accounts/signup/', views.signup, name='signup'),
]
