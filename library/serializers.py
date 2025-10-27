from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from library.models import Author, Book, BookLoan
from users.serializers import UserSerializer


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookShortSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "genre",
        )


class AuthorSerializer(ModelSerializer):
    books_count = serializers.SerializerMethodField()
    books = BookShortSerializer(many=True, read_only=True)

    def get_books_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Author
        fields = "__all__"


class BookLoanSerializer(ModelSerializer):
    borrower = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BookLoan
        fields = "__all__"
