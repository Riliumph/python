from django.urls import include, path

from user_mng_app.controller import bulk_d, lc, rud

urlpatterns = [
    path('v1/users/', lc.ListCreate.as_view()),
    path('v1/users/<int:user_id>', rud.GetUpdateDestroy.as_view()),
    path('v1/users/delete', bulk_d.BulkDelete.as_view()),
]
