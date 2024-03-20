# to be run in terminal

import pickle
import requests

from kinopoisk_api import API_key as API_key

with open('movies_list.pkl', 'rb') as file:
    movies_list = pickle.load(file)

url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'

headers = {
  'X-API-KEY': API_key,
  'Content-Type': 'application/json',
}

for idx, movie in enumerate(movies_list):
    movie_url = url + '/' + str(movie['kinopoiskId'])
    response = requests.get(movie_url, headers=headers).json()
    description = response.get('description')
    if description is None:
        description = response.get('shortDescription')
    movie['description'] = description


with open('movies_list.pkl', 'wb') as file:
    pickle.dump(movies_list, file)
