from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BookLoan
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework.decorators import action
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.models import Author, Book, BookLoan
from library.serializers import (AuthorSerializer, BookSerializer,
                                   BookLoanSerializer)


class AuthorViewSet(ModelViewSet):
    """Вьюсет для модели автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        """метод распределения прав доступа"""
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = (IsAdminUser,)
        elif self.action in ["retrieve", "list"]:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class BookCreateApiView(CreateAPIView):
    """Класс контроллера для создания книги администратором"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)


class BookListApiView(ListAPIView):
    """Класс контроллера для вывода списка книг для всех пользователей"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = AllowAny


class BookRetrieveApiView(RetrieveAPIView):
    """Класс контроллера для вывода экземпляра книги для авторизованных пользователей"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)


class BookUpdateApiView(UpdateAPIView):
    """Класс контроллера для изменения экземпляра книги администратором"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)


class BookDestroyApiView(DestroyAPIView):
    """Класс контроллера для удаления экземпляра книги администратором"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)


class BookLoanCreateApiView(CreateAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def borrow_book(request, book_id):
        """Функция описания выдачи книги"""
        book = get_object_or_404(Book, pk=book_id)
        # Проверяем, что книга доступна
        if book.is_available == 'available':
            # Создаем запись в журнале выдачи книг
            loan = BookLoan.objects.create(
                book=book, borrower=request.user,
                due_date=timezone.now().date()+30)

            # Обновляем статус книги на "Выдана"
            book.is_available = 'on_loan'
            book.save()

class BookLoanUpdateApiView(UpdateAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def return_book(request, loan_id):
        """Функция описания возврата книги"""
        loan = get_object_or_404(BookLoan, id=loan_id)
        # Проверяем, что книга не была возвращена ранее
        if loan.return_date is None:
            # Устанавливаем текущую дату как дату возврата
            loan.return_date = timezone.now().date()
            loan.save()

            # Обновляем статус книги на "доступна"
            book = loan.book
            book.is_available = 'available'
            book.save()

            # Проверяем была ли просрочка
            if loan.return_date > loan.due_date:
                # При каждой просрочке увеличиваем количество просрочек
                user = loan.borrower
                user.number_of_delays += 1
                # Если просрочек больше 5 блокируем пользователя
                if user.number_of_delays > 5:
                    user.is_active = False
                    user.save()
