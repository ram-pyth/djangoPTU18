from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Book, BookInstance, Genre


def index(request):
    # suskaičiuojam knygas ir jų egzempliorius
    num_books = Book.objects.count()
    num_bookinstances = BookInstance.objects.count()

    # autorių skaičius
    num_authors = Author.objects.count()

    # suskaičiuojam laisvus knygų egzempliorius(statusas = 'g')
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    context_my = {
        'num_books_t': num_books,
        'num_bookinstances_t': num_bookinstances,
        'num_authors_t': num_authors,
        'num_instances_available_t': num_instances_available
    }
    return render(request, 'index.html', context=context_my)


def authors(request):
    authors_objs = Author.objects.all()
    context = {
        'authors_t': authors_objs
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author_obj': single_author})


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list" # standartinis pavadinimas, sukuriamas django automatiškai
    template_name = "book_list.html"


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = "book" # standartinis pavadinimas, sukuriamas django automatiškai
    template_name = "book_detail.html"




