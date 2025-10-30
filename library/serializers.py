from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from library.models import Author, Book, BookLoan


class BookSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="name_author", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookShortSerializer(ModelSerializer):
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
    books_count = serializers.SerializerMethodField()
    books = BookShortSerializer(many=True, read_only=True)

    def get_books_count(self, obj):
        return obj.books.count()

    class Meta:
        model = Author
        fields = "__all__"


class BookLoanSerializer(ModelSerializer):
    issue_date = serializers.DateField(read_only=True)
    due_date = serializers.DateField(read_only=True)

    class Meta:
        model = BookLoan
        fields = "__all__"
