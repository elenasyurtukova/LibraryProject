from django.contrib import admin

from library.models import Author, Book, BookLoan


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name_author", "bio", "created_at", "updated_at")
    list_filter = ("name_author", "bio")
    search_fields = ("name_author", "bio")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "is_available")
    list_filter = ("title", "author", "genre", "is_available")
    search_fields = ("title", "author", "genre")

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ("book", "author", "borrower", "issue_date", "due_date", "return_date")
    list_filter = ("book", "author", "borrower", "issue_date", "due_date", "return_date")
    search_fields = ("book", "author", "borrower")