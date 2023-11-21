from django.urls import path

from book_mng_app.controller import book, book_genre, genre

urlpatterns = [
    path('v1/genres/', genre.GetAllCreate.as_view()),
    path('v1/genres/<int:genre_id>', genre.GetUpdateDestroy.as_view()),
    path('v1/books/', book.GetAllCreate.as_view()),
    path('v1/books/<int:book_id>', book.GetUpdateDestroy.as_view()),
]
