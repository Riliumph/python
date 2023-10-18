from django.urls import include, path

from user import controller

urlpatterns = [
    path('v1/users/', controller.GetAllCreate.as_view()),
    path('v1/users/<int:user_id>', controller.GetUpdateDestroy.as_view()),
    path('v1/users/delete', controller.BulkDelete.as_view()),
]
