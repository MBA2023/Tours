from datetime import datetime

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from tours.forms import BookForm
from tours.models import Tour, Schedule
from tours.services import get_full_schedule, get_all_active_tours, get_tour_slots, book_user_on_tour


def get_all_tours(request):
    if request.method == 'GET':
        tours = get_all_active_tours()
        # Вернуть html со всеми турами
        return render(request, 'tours/index.html', context=dict(tours=tours))


def get_tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    available_times = tour.slots_str.split(',')
    free_slots = get_tour_slots(tour)
    # freeSlots - Полуить из Бд связанные с туром Schedule и привести его к формату котррый нужен на фронте (в шаблоне)
    return render(
        request,
        'tours/tour_detail.html',
        context=dict(tour=tour, available_times=available_times, free_slots=free_slots)
    )


def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'GET':
        return render(request, 'tours/book.html', context=dict(tour=tour, start_time=request.GET.get('d')))

    form = BookForm(request.POST)
    if form.is_valid():
        start_time = form.cleaned_data.pop('start_time')
        participant_create, schedule_create = book_user_on_tour(tour, form.cleaned_data, start_time)

        return render(request, 'tours/book_result_success.html', context=dict(
            tour=tour,
            participant_create=participant_create,
            schedule_create=schedule_create
        ))



