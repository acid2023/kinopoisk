from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, QueryDict

from kinopoisk.models import Genre

def get_request_body(request: HttpRequest) -> QueryDict | HttpResponse:
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return request.POST
    else:
        return HttpResponseBadRequest('Wrong request method')


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