from django.urls import path

from book_management.genres import controller

urlpatterns = [
    path('', controller.GetAllCreate.as_view()),
    path('<int:genre_id>', controller.GetUpdateDestroy.as_view()),
]