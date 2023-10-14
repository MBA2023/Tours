from django.urls import path

from tours.views import get_all_tours, get_tour_detail, book_tour


urlpatterns = [
    path('', get_all_tours, name='index'),
    path("tours/<int:tour_id>/", get_tour_detail, name='tour_detail'),
    path("tours/<int:tour_id>/book/", book_tour, name='tour_booking'),
]
