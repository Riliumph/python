from django.urls import path

from sample_app.genres import controller

urlpatterns = [
    path('', controller.GetAllCreate.as_view()),
    path('<int:genre_id>', controller.GetUpdateDestroy.as_view()),
]
