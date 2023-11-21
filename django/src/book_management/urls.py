from django.urls import include, path

urlpatterns = [
    path('v1/genres/', include("book_management.genres.urls")),
    path('v1/books/', include("book_management.books.urls")),
]
