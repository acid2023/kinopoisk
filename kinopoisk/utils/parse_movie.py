# to be run in terminal


import requests
import pickle

from kinopoisk_api import API_key as API_key  # type: ignore

url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'
qurl = 'https://kinopoiskapiunofficial.tech/api/v2.2/films?order=RATING&type=ALL&ratingFrom=9.8&page=2'
headers = {
  'X-API-KEY': API_key,
  'Content-Type': 'application/json',
  'type': 'FILM', 'page': 2,
}

response = requests.get(qurl, headers=headers)  # type: ignore
response = response.json().get('items')
for item in response:
    print(item)
with open('movies_list.pkl', 'wb') as file:
    pickle.dump(response, file)
