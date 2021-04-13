from django.shortcuts import render
from actors.forms import ActorSearchForm
from IMDB.settings import OMDB_KEY, TMDB_KEY, SECRET_KEY
import requests
# Create your views here.


base_url = 'https://api.themoviedb.org/3'

def search_actor(request):
    if request.method == 'POST':
        form = ActorSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            actor_name = data['search_actor']
            id_path = f'/search/person'
            endpoint = f'{base_url}{id_path}?api_key={TMDB_KEY}&query={actor_name}'
            id_request = requests.get(endpoint)
            if id_request.status_code in range(200, 299):
                request_data = id_request.json()
                results = request_data['results']
                return render(request, 'actors/actor_results.html', {'results': results})
    form = ActorSearchForm()
    return render(request, 'homepage.html', {'form': form})

def actor_detail(request, actor_id):
    actor_path = f'/person/{actor_id}'
    actor_endpoint = f'{base_url}{actor_path}?api_key={TMDB_KEY}'
    actor_request = requests.get(actor_endpoint)
    if actor_request.status_code in range(200, 299):
        actor_data = actor_request.json()
        return render(request, 'actors/actor_detail.html', {'actor': actor_data})

def actor_link(request, actor_name):
    id_path = f'/search/person'
    endpoint = f'{base_url}{id_path}?api_key={TMDB_KEY}&query={actor_name}'
    id_request = requests.get(endpoint)
    results = []
    if id_request.status_code in range(200, 299):
        request_data = id_request.json()
        results = request_data['results']
    for result in results:
        if result['name'] == actor_name:
            actor_id = result['id']
            actor_path = f'/person/{actor_id}'
            actor_endpoint = f'{base_url}{actor_path}?api_key={TMDB_KEY}'
            actor_request = requests.get(actor_endpoint)
            if actor_request.status_code in range(200, 299):
                actor_data = actor_request.json()
            return render(request, 'actors/actor_detail.html', {'actor': actor_data})


    

