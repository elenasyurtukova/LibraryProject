from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BookLoan
from django.utils import timezone

def borrow_book(request, book_id):
    """Функция описания выдачи книги"""
    book = get_object_or_404(Book, pk=book_id)
    # Проверяем, что книга доступна
    if book.is_available == 'available':
        # Создаем запись в журнале выдачи книг
        loan = BookLoan.objects.create(book=book, borrower=request.user, due_date=timezone.now().date()+30)

        # Обновляем статус книги на "Выдана"
        book.is_available = 'on_loan'
        book.save()

def return_book(request, loan_id):
    """Функция описания возврата книги"""
    loan = get_object_or_404(BookLoan, id=loan_id)
    if request.method == 'POST':
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
