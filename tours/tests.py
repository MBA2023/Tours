from datetime import datetime

from django.test import TestCase

from faker import Faker

from tours.models import Tour, Schedule
from tours.services import get_tour_slots
from users.models import Participant


class TestGetTourSlots(TestCase):

    faker = Faker()

    def setUp(self):
        self.tour_times = [':'.join(self.faker.time().split(':')[0:2]) for num in range(3)]
        self.tour = Tour.objects.create(
            name=self.faker.sentence(),
            description=self.faker.paragraph(),
            slots_str=','.join(self.tour_times)
        )
        self.participants = Participant.objects.bulk_create(
            [Participant(fio=self.faker.name(), phone=self.faker.phone_number()) for i in range (3)]
        )

    def get_expected_from_schedules(self, schedules):
        result = {}
        for schedule in schedules:
            # print(f"{result=}")
            # print(f"{schedule['start_time']=}")
            schedule_date = schedule['start_time'].date().isoformat()
            # print(f"{schedule_date=}")
            schedule_time = schedule['start_time'].strftime('%H:%M')
            # print(f"{schedule_time=}")
            date_schedule = result.get(schedule_date, {})
            if not date_schedule:
                result[schedule_date] = {schedule_time: self.tour.max_participants - 1}
                continue
            times = date_schedule.get(schedule_date, {})
            # print(f"{times=}")
            if times.get(schedule_time):
                times[schedule_time] -= 1
            else:
                times[schedule_time] = self.tour.max_participants - 1
        return result

    def test_get_tour_slots_success(self):
        expected_dates = [datetime.strptime(
            f"{self.faker.date()}T{tour_time}",
            '%Y-%m-%dT%H:%M'
        ) for tour_time in self.tour_times]
        expected_schedules = [
            dict(tour=self.tour, participant=self.participants[0], start_time=expected_dates[0]),
            dict(tour=self.tour, participant=self.participants[1], start_time=expected_dates[1]),
            dict(tour=self.tour, participant=self.participants[2], start_time=expected_dates[2]),

        ]
        schedules = Schedule.objects.bulk_create([Schedule(**data) for data in expected_schedules])
        expected = self.get_expected_from_schedules(expected_schedules)
        result = get_tour_slots(self.tour)

        self.assertEqual(result, expected)

