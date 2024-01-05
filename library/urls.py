from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("authors/", views.authors, name="authors-all"),
    path("authors/<int:author_id>", views.author, name="author-one"),
    path("books/", views.BookListView.as_view(), name="books-all"),
]
