from django.urls import path, include
from sample_app.users import controller

urlpatterns = [
    path('v1/users/', include("sample_app.users.urls")),
]
