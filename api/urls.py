from django.urls import path
from .views import tasks, get_task

urlpatterns = [
    path('tasks/', tasks),
    path('tasks/<int:pk>/', get_task),
]
