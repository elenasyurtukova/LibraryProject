from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from library.models import Author, Book, BookLoan


class BookSerializer(ModelSerializer):
    """Класс сериализатора для модели книги"""
    author = serializers.SlugRelatedField(slug_field="name_author", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookShortSerializer(ModelSerializer):
    """Класс сериализатора для модели книги в сокращенном варианте"""
    author = serializers.SlugRelatedField(slug_field="name_author", read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "author",
            "title",
            "genre",
        )


class AuthorSerializer(ModelSerializer):
    """Класс сериализатора для модели автора"""
    books_count = serializers.SerializerMethodField()
    books = BookShortSerializer(many=True, read_only=True)

    def get_books_count(self, obj):
        """Класс-метод подсчета количества книг у заданного автора"""
        return obj.books.count()

    class Meta:
        model = Author
        fields = "__all__"


class BookLoanSerializer(ModelSerializer):
    """Класс сериализатора для модели выдачи книги"""
    issue_date = serializers.DateField(read_only=True)
    due_date = serializers.DateField(read_only=True)

    class Meta:
        model = BookLoan
        fields = "__all__"
