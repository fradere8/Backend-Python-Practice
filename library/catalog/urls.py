from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
]