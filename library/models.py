from django.db import models


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Book(models.Model):
    """Modelis reprezentuoja knygą-leidinį, ne konkretų
    bibliotekos turimą fizinį egzempliorių"""
    title = models.CharField('Pavadinimas', max_length=150)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField('Genre', help_text='Išrinkite knygai žanrus')

    def __str__(self):
        return f'{self.title}'


class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=20, help_text='Įveskite žanro pavadinimą')

    def __str__(self):
        return f'{self.name}'
