from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField
from datetime import date
import uuid
from PIL import Image


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    # description = models.TextField('Aprašymas', max_length=2000, default="biografija..")
    description = HTMLField()

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
    title = models.CharField(_('Title'), max_length=150)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    summary = models.TextField(_('Summary'), max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 simbolių <a href="https://en.wikipedia.org/wiki/ISBN">ISBN wiki</a>')
    genre = models.ManyToManyField('Genre', help_text='Išrinkite knygai žanrus')
    cover = models.ImageField(_('Cover'), upload_to='covers', null=True, blank=True)

    def display_genre(self):
        return ', '.join(el.name for el in self.genre.all())

    display_genre.short_description = _("Genres")

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
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True) # auto related_name - bookinstance_set
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='a', help_text='Statusas')
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    class Meta:
        ordering = ['due_back', ]

    def __str__(self):
        return f'{self.id} {self.book}'


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profilis'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 200 or img.width > 200:
            new_size = (200, 200)
            img.thumbnail(new_size)
            img.save(self.picture.path)

