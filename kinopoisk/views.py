from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.db.models import Q

from kinopoisk.forms import MovieForm
from kinopoisk.models import Movie, Genre


def add_new_movie(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse({'status': 'ok'})
        else:
            return HttpResponseBadRequest(form.errors.as_json())
    else:
        form = MovieForm()
    return render(request, 'movie_create.html', {'form': form})


def view_movie(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = Movie.objects.get(id=movie_id)
    genres = ', '.join([a.genre for a in movie.genre.all()])
    image_url = movie.cover.url
    return render(request, 'movie.html', {'movie': movie, 'genres': genres, 'image_url': image_url})


def get_filters_from_request(input_request: HttpRequest) -> dict[str, str | str | list[str] | None] | HttpResponse:

    filters: dict[str, str | list[str] | None] = {}

    if input_request.method == 'GET':
        request = input_request.GET
    elif input_request.method == 'POST':
        request = input_request.POST
    else:
        return HttpResponseBadRequest('Wrong request method')

    if 'year' in request:
        value = request['year']
        if value is None or value == '':
            filters['year'] = None
        else:
            filters['year'] = value

    if 'genres' in request:

        genres_in_request = request['genres']
        genres = [genre.strip() for genre in genres_in_request.split(",")]

        valid_genres = list(Genre.objects.values_list('genre', flat=True))
        checked_genres = [genre for genre in genres if genre in valid_genres]

        filters['genre'] = checked_genres

    if 'rating' in request:
        value = request['rating']
        if value is None or value == '':
            filters['rating'] = None
        else:
            filters['rating'] = value

    return filters


def view_movies(request: HttpRequest) -> HttpResponse:
    filters = get_filters_from_request(request)

    if isinstance(filters, HttpResponse):
        return filters
    movies = Movie.objects.all()
    for filter, value in filters.items():
        if filter == 'genre' and value is not None:
            q_list = Q()
            for genre in value:
                q_list |= Q(genre__genre=genre)
            movies = movies.filter(q_list).distinct()
        elif filter == 'year' and value is not None:
            movies = movies.filter(year=value)
        elif filter == 'rating' and value is not None:
            movies = movies.filter(rating=value)

    content = [movie for movie in movies]
    return render(request, 'movies.html', {'content': content})


def view_search(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        request_body = request.GET
    elif request.method == 'POST':
        request_body = request.POST
    else:
        return HttpResponseBadRequest('Wrong request method')

    search = request_body.get("search", None)

    if search is None or search == "":
        return HttpResponseBadRequest("'search' as required parameter is missing or search query is empty")

    query_words = [query.strip() for query in search.split(",")]

    search_behavior = request_body.get("behavior", None)

    try:
        query_results = Movie.objects.all()
        iterated_query = Movie.objects.none()

        for word in query_words:

            if search_behavior is None or search_behavior == 'loose':
                iterated_query |= query_results.filter(Q(title__icontains=word) | Q(description__icontains=word))

            elif search_behavior == 'strict':
                word = r'\b' + word + r'\b'
                iterated_query |= query_results.filter(Q(title__iregex=word) | Q(description__iregex=word))

            else:
                return HttpResponseBadRequest('please specify search behavior - "behavior" key should be either "strict" or "loose"')

        query_results = iterated_query

        if not query_results.exists():
            return HttpResponseNotFound('Your request resulted in no results')
        else:
            content = [movie for movie in query_results]
            return render(request, 'movies_search.html', {'content': content, 'search': search})

    except Movie.DoesNotExist:
        return HttpResponseNotFound('Your request resulted in no results')
