from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    # make a path for book_rating
    path('book_rating/<int:book_id>', views.book_rating, name='book_rating'),
    path('about', views.about, name='about'),
    # alias for legacy link
    path('aboutus', views.about, name='aboutus'),
    path('search', views.search_books, name='search_books'),
    path('person/<slug:slug>/', views.person_profile, name='person'),
]

