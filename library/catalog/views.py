from datetime import datetime
from django.http import Http404
from django.shortcuts import render


BOOKS = {
    1: {
        'id': 1,
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
        'published_date': datetime(1967, 3, 14),
        'pages': 480,
        'description': 'Роман о добре и зле, любви и трусости.',
        'available': True,
    },
    2: {
        'id': 2,
        'title': 'Преступление и наказание',
        'author': 'Фёдор Достоевский',
        'published_date': datetime(1866, 6, 21),
        'pages': 671,
        'description': 'История бывшего студента Раскольникова.',
        'available': False,
    },
}


def book_detail(request, book_id):
    try:
        book = BOOKS[book_id]
    except KeyError:
        raise Http404('Книга не найдена')

    return render(request, 'catalog/book_detail.html', {'book': book})
