# to be run in termminal

import pickle
import requests

with open('movies_list.pkl', 'rb') as file:
    movies_list = pickle.load(file)

for idx, movie in enumerate(movies_list):
    title = movie['nameRu']

    if title is None:
        title = movie['nameEn']
    if title is None:
        title = movie['nameOriginal']
    image_url = movie['posterUrl']
    image = requests.get(image_url).content
    filename = f"{movie['kinopoiskId']}.jpg"
    with open(filename, 'wb') as file:
        file.write(image)
    print(f"Downloaded {filename}")
