from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=128)

    def __str__(self):
        return self.genre


class Movie(models.Model):
    title = models.CharField(max_length=512)
    kinopoiskID = models.IntegerField()
    year = models.SmallIntegerField()
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    genre = models.ManyToManyField(Genre)
    cover = models.ImageField(upload_to="covers/", null=True, blank=True)

    def __str__(self):
        return f'{self.title} ({self.year})'

    def get_genres(self):
        return ', '.join([genre.genre for genre in self.genre.all()])
