from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("authors/", views.authors, name="authors-all"),
    path("authors/<int:author_id>", views.author, name="author-one"),
    path("books/", views.BookListView.as_view(), name="books-all"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name="book-one"),
    path("search/", views.search, name="search"),

    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path("register/", views.register_user, name="register-url"),
    path("profilis/", views.profilis, name="profilis-url"),
    path("mybooks/new", views.BookByUserCreateView.as_view(), name="my-borrowed-new"),
    path("mybooks/<uuid:pk>", views.BookByUserUpdateView.as_view(), name="my-borrowed-update"),
    path("mybooks/<uuid:pk>/delete", views.BookByUserDeleteView.as_view(), name="my-borrowed-delete"),

    path("books/<uuid:pk>/delete", views.BookByGroupDeleteView.as_view(), name="bookinstance-delete"),
]



