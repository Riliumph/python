from django.urls import path

from sample_app.users import controller

urlpatterns = [
    path('', controller.GetAllCreate.as_view()),
    path('<int:user_id>', controller.GetUpdateDestroy.as_view()),
    path('delete', controller.BulkDelete.as_view()),
]
