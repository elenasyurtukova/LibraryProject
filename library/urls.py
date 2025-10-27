from django.urls import path
from rest_framework.routers import SimpleRouter

from library.apps import LibraryConfig
from library.views import (AuthorViewSet, BookCreateApiView,
                             BookDestroyApiView, BookListApiView,
                             BookRetrieveApiView, BookUpdateApiView,
                             BookLoanCreateApiView, BookLoanUpdateApiView)

app_name = LibraryConfig.name

router = SimpleRouter()
router.register("", AuthorViewSet)

urlpatterns = [
    path("books/", BookListApiView.as_view(), name="books_list"),
    path("books/<int:pk>/", BookRetrieveApiView.as_view(), name="book_retrieve"),
    path("books/create/", BookCreateApiView.as_view(), name="book_create"),
    path(
        "books/<int:pk>/delete/", BookDestroyApiView.as_view(), name="book_delete"
    ),
    path(
        "books/<int:pk>/update/", BookUpdateApiView.as_view(), name="book_update"
    ),
    path("bookloan/", BookLoanCreateApiView.as_view(), name="bookloan_create"),
    path("bookloan/<int:pk>/update/", BookLoanUpdateApiView.as_view(), name="bookloan_update")
]
urlpatterns += router.urls
