from django.urls import path, include

from .views import Movie, RecommendedMovie

urlpatterns = [
    path('movie/', Movie.as_view(), name='movie'),  # movie
    path('recommended-movie/', RecommendedMovie.as_view(), name='movie'),  # movie
]