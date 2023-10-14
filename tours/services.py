from django.db import transaction
from django.db.models import Count

from tours.models import Schedule, Tour
from tours.utils import get_map_from_list
from users.models import Participant


def get_full_schedule():
    schedule = Schedule.objects.select_related('tour', 'tour__guide').all()
    # Как ДЗ найти способ не вытягивать из БД лишние поля, например tour.price, tour.description и т.д.
    # for slot in schedule:
    #     print(slot.tour.name)
    # print(f">>> {str(schedule.query)}")
    return schedule


def get_all_active_tours():
    return Tour.objects.all()


def get_tour_slots(tour):
    """
    Найти все записи для данного тура и вернуть в виде:
    {
        '2023-10-02': {
            '8:00': 0,
            '9:00': 5,
            '10:00': 10
        },
        '2023-10-15': {
            '8:00': 1,
            '9:00': 5,
            '10:00': 10
        }
    }
    """
    schedules_by_start_time = Schedule.objects.values('start_time').annotate(slots_for_start_time=Count('id')).filter(
        tour=tour).values('slots_for_start_time', 'start_time')
    schedules_by_start_time_map = get_map_from_list(
        schedules_by_start_time,
        lambda schedule: schedule.get('start_time').date().isoformat()
    )
    result = {}
    for start_time, schedule in schedules_by_start_time_map.items():
        result[start_time] = get_map_from_list(
            schedule,
            lambda slot: slot['start_time'].strftime('%H:%M'),
            lambda slot: tour.max_participants - slot['slots_for_start_time']
        )
        for slot_time, slots in result[start_time].items():
            result[start_time][slot_time] = slots[0]

    return result


def book_user_on_tour(tour, participant_data, start_time):
    with transaction.atomic():
        participant, participant_create = Participant.objects.get_or_create(**participant_data)
        schedule, schedule_create = Schedule.objects.get_or_create(tour=tour, participant=participant, start_time=start_time)
    return participant_create, schedule_create
