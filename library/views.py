from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Author, Book, BookInstance, Genre, BookReview
from .forms import BookReviewForm, UserUpdateForm, ProfileUpdateForm, UserBookCreateForm


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
    context_object_name = "book_list"  # standartinis pavadinimas, sukuriamas django automatiškai
    template_name = "book_list.html"
    paginate_by = 4


class BookDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Book
    context_object_name = "book"  # standartinis pavadinimas, sukuriamas django automatiškai
    template_name = "book_detail.html"
    form_class = BookReviewForm

    # post metodas formai
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # formos custom validacija
    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

    # kur nueinam po formos submito
    def get_success_url(self):
        return reverse('book-one', kwargs={'pk': self.object.id})


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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).order_by('due_back')


@csrf_protect
def register_user(request):
    if request.method != "POST":
        return render(request, 'registration/registration.html')

    # jeigu POST
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    password2 = request.POST["password2"]

    if password != password2:
        messages.error(request, "Slaptažodžiai nesutampa!!!")

    if User.objects.filter(username=username).exists():
        messages.error(request, f"Vartotojo vardas {username} užimtas!!!")

    if User.objects.filter(email=email).exists():
        messages.error(request, f"Emailas {email} jau registruotas!!!")

    if messages.get_messages(request):
        return redirect('register-url')

    User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, f"Vartotojas vardu {username} sukurtas!!!")
    return redirect('login')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas!")
            return redirect('profilis-url')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profilis.html', context=context)


class BookByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    success_url = '/library/mybooks'
    template_name = 'user_book_form.html'
    form_class = UserBookCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)


class BookByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    success_url = '/library/mybooks'
    template_name = 'user_book_form.html'
    form_class = UserBookCreateForm
    # fields = ('book', 'due_back') # alternatyva form_class = UserBookCreateForm, tinka greitam testavimui

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bookinstance_o = self.get_object()  # pagaunam esamą model = BookInstance objektą
        return bookinstance_o.reader == self.request.user  # patikrinimas ar django useris sutampa su knygos kopijai prirašytu
