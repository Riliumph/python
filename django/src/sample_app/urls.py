from django.urls import path, include
from sample_app.users import views

urlpatterns = [
    path('v1/users', views.UsersGetAllOrPost.as_view()),
]
