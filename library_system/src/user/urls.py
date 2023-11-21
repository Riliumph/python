from django.urls import include, path

from user.controller import bulk_controller, controller, id_controller

urlpatterns = [
    path('v1/users/', id_controller.GetAllCreate.as_view()),
    path('v1/users/<int:user_id>', controller.GetUpdateDestroy.as_view()),
    path('v1/users/delete', bulk_controller.BulkDelete.as_view()),
]
