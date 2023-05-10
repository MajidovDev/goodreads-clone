from django.contrib import admin
from .models import Book, BookAuthor, BookReview, Author


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn', 'description')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('author',)
    list_display = ('book', 'author')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user', 'starts_given', 'book', )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)

