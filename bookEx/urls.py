# bookMng/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),                              # shows displaybooks.html
    path("books/", views.displaybooks, name="display-books"),        # optional: direct list route
    path("books/my/", views.mybooks, name="my-books"),               # your mybooks view
    path("postbook", views.postbook, name="postbook"),               # keep same path you used
    path("book_delete/<int:book_id>", views.book_delete, name="book_delete"),
]
