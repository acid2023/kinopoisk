# to be run in django shell

import pickle

from django.core.files import File
from kinopoisk.models import Movie, Genre


with open('movies_list.pkl', 'rb') as file:
    movies_list = pickle.load(file)

for idx, movie in enumerate(movies_list):
    title = movie['nameRu']
    if title is None:
        title = movie['nameOriginal']
    description = movie.get('description', None)
    if description is None:
        descriptin = movie.get('shortDescription', None)
    rating = movie["ratingKinopoisk"]
    if rating is None:
        rating = movie["ratingImdb"]
    the_movie = Movie.objects.create(
        title=title,
        year=movie['year'],
        description=description,
        rating=rating,
        kinopoiskID=movie['kinopoiskId']
        )
    print(the_movie)
    the_movie.save()
    filename = str(movie['kinopoiskId']) + '.jpg'
    with open(filename, 'rb') as file:
        the_movie.cover = File(file, filename)
        the_movie.save()
    movie_genres = [item.get('genre') for item in movie.get('genres')]
    genre_list = [genre.id for genre in Genre.objects.all() if genre.genre in movie_genres]
    for genre_id in genre_list:
        genre = Genre.objects.get(id=genre_id)
        the_movie.genre.add(genre)
    the_movie.save()
