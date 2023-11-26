from django.urls import path

from book_mng_app.controller import book, book_genre, genre

urlpatterns = [
    path('v1/genres/', genre.ListCreate.as_view()),
    path('v1/genres/<int:genre_id>', genre.GetUpdateDestroy.as_view()),
    path('v1/books/', book.ListCreate.as_view()),
    path('v1/books/<int:book_id>', book.GetUpdateDestroy.as_view()),
    path('v1/books/<int:book_id>/genres',
         book_genre.ListCreate.as_view()),
    path('v1/books/<int:book_id>/genres/<int:genre_id>',
         book_genre.GetDestroy.as_view()),

]
