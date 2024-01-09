from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Author, Book, BookInstance, Genre


def index(request):
    # suskaičiuojam knygas ir jų egzempliorius
    num_books = Book.objects.count()
    num_bookinstances = BookInstance.objects.count()

    # autorių skaičius
    num_authors = Author.objects.count()

    # suskaičiuojam laisvus knygų egzempliorius(statusas = 'g')
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # skaičiuojam kiek kartų vartotojas prisijungė prie puslapio
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context_my = {
        'num_books_t': num_books,
        'num_bookinstances_t': num_bookinstances,
        'num_authors_t': num_authors,
        'num_instances_available_t': num_instances_available,
        'num_visits_t': num_visits,
    }
    return render(request, 'index.html', context=context_my)


def authors(request):
    authors_objs = Author.objects.all()
    paginator = Paginator(authors_objs, 2)
    page_number = request.GET.get('page')
    paged_authors_objs = paginator.get_page(page_number)
    context = {
        'authors_t': paged_authors_objs
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author_obj': single_author})


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list" # standartinis pavadinimas, sukuriamas django automatiškai
    template_name = "book_list.html"
    paginate_by = 4


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = "book" # standartinis pavadinimas, sukuriamas django automatiškai
    template_name = "book_detail.html"


def search(request):
    query_text = request.GET.get("search_text", "")
    search_results = Book.objects.filter(Q(title__icontains=query_text) |
                                         Q(summary__icontains=query_text) |
                                         Q(author__last_name__icontains=query_text))
    context_t = {
        "book_objects": search_results,
        "query_text_t": query_text
    }
    return render(request, "search.html", context=context_t)




