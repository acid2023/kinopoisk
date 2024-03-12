# to be run in django shell

from django.db.models import Count, Min
from django.db.models.functions import Coalesce

from kinopoisk.models import Movie

duplicate_movies = Movie.objects.values('kinopoiskID').annotate(
    null_count=Count(Coalesce('description', 'rating', 'cover')),
    min_id=Min('id')).filter(null_count__gt=0).order_by('kinopoiskID', '-null_count')

for movie in duplicate_movies:
    Movie.objects.filter(kinopoiskID=movie['kinopoiskID']).exclude(id=movie['min_id']).delete()
