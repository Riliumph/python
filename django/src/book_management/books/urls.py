from django.urls import path

from book_management.books import controller

urlpatterns = [
    path('', controller.GetAllCreate.as_view()),
    path('<int:book_id>', controller.GetUpdateDestroy.as_view()),
    path('<int:book_id>/genres', controller.BookGenreGetAllCreate.as_view()),
]
