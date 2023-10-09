from django.urls import path, include
from sample_app.users import controller

urlpatterns = [
    path('', controller.GetAllCreate.as_view()),
    path('<int:user_id>', controller.GetUpdateDestroy.as_view()),
]
