from django.utils import timezone
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.models import Author, Book, BookLoan
from library.serializers import (AuthorSerializer, BookLoanSerializer,
                                 BookSerializer, BookShortSerializer)


class AuthorViewSet(ModelViewSet):
    """Вьюсет для модели автора"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        """Метод распределения прав доступа"""
        if self.action in ["create", "update", "partial_update", "destroy"]:
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
    serializer_class = BookShortSerializer
    permission_classes = (AllowAny,)


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
    """Класс контроллера для создания записи выдачи книги авторизованным пользователем"""
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Функция с описанием логики выдачи книги и создания записи в журнале выдачи"""
        book_id = request.data.get("book")
        book = get_object_or_404(Book, pk=book_id)
        if book.is_available == "available":
            if not BookLoan.objects.filter(book=book, return_date=None).exists():
                BookLoan.objects.create(book=book, borrower=request.user)
                book.is_available = "on_loan"
                book.save()
                return Response({"message": "Книга успешно выдана!"}, status=201)
            else:
                book.is_available = "on_loan"
                book.save()
                return Response(
                    {"error": "Книга уже выдана другому пользователю."}, status=400
                )
        else:
            return Response({"error": "Книга не доступна."}, status=400)


class BookLoanUpdateApiView(UpdateAPIView):
    """Класс контроллера для изменения записи выдачи книги администратором"""
    serializer_class = BookLoanSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        """Функция с описанием логики возврата книги"""
        loan_id = kwargs.get("loan_id")
        loan = get_object_or_404(BookLoan, id=loan_id)

        # Проверяем, что книга не была возвращена ранее
        if loan.return_date is None:
            # Устанавливаем текущую дату как дату возврата
            loan.return_date = timezone.now().date()
            loan.save()

            # Обновляем статус книги на "доступна"
            book = loan.book
            book.is_available = "available"
            book.save()

            # Проверяем была ли просрочка
            if loan.return_date > loan.due_date:
                # При каждой просрочке увеличиваем количество просрочек
                user = loan.borrower
                user.number_of_delays += 1
                # Если просрочек больше 5, блокируем пользователя
                if user.number_of_delays > 5:
                    user.is_active = False
                user.save()

            return Response({"message": "Книга успешно возвращена!"}, status=200)
        else:
            return Response({"error": "Книга уже была возвращена."}, status=400)


class BookLoanListApiView(ListAPIView):
    """Класс контроллера для вывода списка записей выдачи книг для всех пользователей"""
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BookLoan.objects.all()
        return BookLoan.objects.filter(borrower=self.request.user)
