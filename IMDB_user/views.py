from django.shortcuts import redirect

from IMDB_user.models import MyCustomUser
from movies.models import Movie
import requests


# Create your views here.
tmdb_base_url = 'https://api.themoviedb.org/3'
tmdb_key = 'ea3f0ae618db2e67cd3f57ba270936c4'
omdb_base_url = 'http://www.omdbapi.com/'
omdb_key = 'd361bf3'

# def add_watchlist(request, imbd_id):
#     user = request.user
#     movie = Movie.objects.get(imbd_id=imbd_id)
#     user.watch_list.add(movie)
#     return redirect('/')


def add_favorites(request, movie_id):
    if Movie.objects.filter(tmdb_id=movie_id).exists():
        movie = Movie.objects.get(tmdb_id=movie_id)
        current_user = MyCustomUser.objects.get(id=request.user.id)
        if not current_user.favorites_list.filter(tmdb_id=movie_id).exists():
            current_user.favorites_list.add(movie)
            current_user.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        movie_path = f'/movie/{movie_id}'
        movie_endpoint = f'{tmdb_base_url}{movie_path}?api_key={tmdb_key}'
        movie_request = requests.get(movie_endpoint)
        movie_data = movie_request.json()
        poster = movie_data['poster_path']
        movie = Movie.objects.create(
            tmdb_id = movie_data['id'],
            name = movie_data['title'],
            poster_url = f'https://image.tmdb.org/t/p/w342{poster}'
            
        )
        current_user = MyCustomUser.objects.get(id=request.user.id)
        current_user.favorites_list.add(movie)
        current_user.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def remove_favorites(request, movie_id):
    current_user = MyCustomUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(tmdb_id=movie_id)
    current_user.favorites_list.remove(movie)
    current_user.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    