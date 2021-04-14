from django.shortcuts import redirect, render
from movies.models import Movie
from reviews.models import Review
import requests

from IMDB_user.models import MyCustomUser



# Create your views here.
tmdb_base_url = 'https://api.themoviedb.org/3'
tmdb_key = 'ea3f0ae618db2e67cd3f57ba270936c4'
omdb_base_url = 'http://www.omdbapi.com/'
omdb_key = 'd361bf3'

# Create your views here.
base_url = 'https://api.themoviedb.org/3'
api_key = 'ea3f0ae618db2e67cd3f57ba270936c4'


def add_watchlist(request, tmdb_id):
    user = request.user
    movie = Movie.objects.get(tmdb_id=tmdb_id)
    user.watch_list.add(movie)
    user.save()
    return redirect(f'/movies/{tmdb_id}/')

def remove_watchlist(request, tmdb_id):
    current_user = MyCustomUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(tmdb_id=tmdb_id)
    current_user.watch_list.remove(movie)
    current_user.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

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
    
def profile_view(request):
    watch_list_movies = []
    recomendations = []
    watch_list = request.user.watch_list
    for movie in watch_list.all():
        movie_path = f'/movie/{movie.tmdb_id}'
        movie_endpoint = f'{base_url}{movie_path}?api_key={api_key}'
        movie_request = requests.get(movie_endpoint)
        if movie_request.status_code in range(200, 299):
            movie_data = movie_request.json()
            watch_list_movies.append(movie_data)
            movie_id = movie_data['id']
            recomendations_path = f'/movie/{movie_id}/recommendations'
            recomendations_endpoint = f'{base_url}{recomendations_path}?api_key={api_key}'
            recomendations_endpoint_request = requests.get(
                recomendations_endpoint)
            if recomendations_endpoint_request.status_code in range(200, 299):
                    recomendations_data = recomendations_endpoint_request.json()
                    for recomendations_data in recomendations_data['results']:
                        if not request.user.watch_list.filter(name=recomendations_data['title']):
                            recomendations.append(recomendations_data)
    reviews = Review.objects.filter(user=request.user)
    context = {
            'reviews': reviews,
            'watch_list': watch_list_movies,
            'recomendations': recomendations}
    if watch_list_movies:
        context.update({'test': watch_list_movies[0]})
    if recomendations:
        context.update({'test2': recomendations[0]})
    return render(
        request,
        'profile.html',
        context)
