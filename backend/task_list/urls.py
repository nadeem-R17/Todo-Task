from django.urls import path
from .views import (
    CreateToDoView,
    RetrieveToDoView,
    ListToDoView,
    UpdateToDoView,
    DeleteToDoView,
)

app_name = "todo"

urlpatterns = [
    path("create/", CreateToDoView.as_view(), name="create_todo"),
    path("<int:pk>/", RetrieveToDoView.as_view(), name="retrieve_todo"),
    path("", ListToDoView.as_view(), name="list_todos"),
    path("<int:pk>/update/", UpdateToDoView.as_view(), name="update_todo"),
    path("<int:pk>/delete/", DeleteToDoView.as_view(), name="delete_todo"),
]
