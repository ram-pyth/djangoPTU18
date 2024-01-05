from django.db import models
import uuid


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    description = models.TextField('Aprašymas', max_length=2000, default="biografija..")

    def display_books(self):
        return ', '.join(el.title for el in self.books.all()[:3]) + '...'

    display_books.short_description = "Autoriaus knygos"

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Book(models.Model):
    """Modelis reprezentuoja knygą-leidinį, ne konkretų
    bibliotekos turimą fizinį egzempliorių"""
    title = models.CharField('Pavadinimas', max_length=150)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 simbolių <a href="https://en.wikipedia.org/wiki/ISBN">ISBN wiki</a>')
    genre = models.ManyToManyField('Genre', help_text='Išrinkite knygai žanrus')

    def display_genre(self):
        return ', '.join(el.name for el in self.genre.all())

    display_genre.short_description = "Žanrai"

    def __str__(self):
        return f'{self.title}'


class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=20, help_text='Įveskite žanro pavadinimą')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Žanras'
        verbose_name_plural = 'Žanrai'


class BookInstance(models.Model):
    """Modelis reprezentuojantis konkretų fizinį knygos egzemplorių"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID knygos egzemplioriui')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='a', help_text='Statusas')

    class Meta:
        ordering = ['due_back', ]

    def __str__(self):
        return f'{self.id} {self.book}'
