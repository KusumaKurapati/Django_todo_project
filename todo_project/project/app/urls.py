from django.urls import path
from .import views

urlpatterns = [
    path('register/',view=views.register),
    path('login/',view=views.login),
    path('todoall/',view=views.todoall),
    path('todo_getone/<int:todo_id>',view=views.todo_getone),
    path('create_todo/',view=views.create_todo),
    path('update_todo/<int:todo_id>',view=views.update_todo),
    path('delete_todo/<int:todo_id>',view=views.delete_todo)
]

