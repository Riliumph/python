from django.urls import path

from book_management.books.controller import book_genre, lc, rud

urlpatterns = [
    path('', lc.GetAllCreate.as_view()),
    path('<int:book_id>', rud.GetUpdateDestroy.as_view()),
    path('<int:book_id>/genres', book_genre.BookGenreGetAllCreate.as_view()),
]
