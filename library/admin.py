from django.contrib import admin

from .models import Author, Book, Genre, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # automatiškai kuriamų eilučių skaičius


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'display_genre')
    search_fields = ('title', 'author__last_name')
    inlines = [BookInstanceInline, ]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    readonly_fields = ('id',)
    list_editable = ('status', 'due_back')
    search_fields = ('book__title', 'id')

    fieldsets = (
        ('Knygos egzempliorius', {'fields': ('book',)}),
        ('Prieinamumas', {'fields': ('status', 'due_back')})
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_books')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
