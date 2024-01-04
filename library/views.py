from django.shortcuts import render
from django.http import HttpResponse

from .models import Author, Book, BookInstance, Genre


def index(request):
    # suskaičiuojam knygas ir jų egzempliorius
    num_books = Book.objects.count()
    num_bookinstances = BookInstance.objects.count()

    # autorių skaičius
    num_authors = Author.objects.count()

    context_my = {
        'num_books_t': num_books,
        'num_bookinstances_t': num_bookinstances,
        'num_authors_t': num_authors
    }
    return render(request, 'index.html', context=context_my)
