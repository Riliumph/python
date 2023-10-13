from django.urls import include, path

from sample_app.users import controller

urlpatterns = [
    path('v1/users/', include("sample_app.users.urls")),
    path('v1/genres/', include("sample_app.genres.urls")),
    path('v1/books/', include("sample_app.books.urls")),
]
