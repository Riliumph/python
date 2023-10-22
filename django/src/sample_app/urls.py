from django.urls import include, path

urlpatterns = [
    path('v1/genres/', include("sample_app.genres.urls")),
    path('v1/books/', include("sample_app.books.urls")),
]
