from django.db import models

from config.settings import AUTH_USER_MODEL
from users.models import User


class Author(models.Model):
    name_author = models.CharField(max_length=150, verbose_name="имя автора")
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="биография автора")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_author

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['-created_at'] # Сортировка авторов по дате создания в обратном порядке


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('on_loan', 'Выдана'),
    ]
    title = models.CharField(max_length=200, verbose_name="название книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField(blank=True, null=True, verbose_name="описание книги")
    genre = models.TextField(blank=True, null=True, verbose_name="жанр книги")
    is_available = models.CharField(max_length=10, choices=STATUS_CHOICES,
                                    default='available', verbose_name="флаг доступности книги")

    def __str__(self):
        return f"Автор: {self.author.name} название книги: {self.title}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['author', 'title']

class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Читатель")
    issue_date = models.DateField(auto_now_add=True, verbose_name="дата выдачи")
    due_date = models.DateField(verbose_name="срок возврата")
    return_date = models.DateField(blank=True, null=True, verbose_name="дата возврата")

    class Meta:
        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книг"

    def __str__(self):
        return f"Выдача книги '{self.book.title}' для пользователя {self.borrower.name}"
