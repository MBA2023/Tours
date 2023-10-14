from django.db import models
from django.urls import reverse
from pytils.translit import slugify



def get_tour_main_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<tour_id>/<filename>
    return f"{slugify(instance.name)[:5]}/{filename}"


# Create your models here.
class Tour(models.Model):
    """Таблица экскурсий"""

    guide = models.ForeignKey('tours.Guide', on_delete=models.SET_NULL, null=True)
    provider = models.ForeignKey('tours_parser.ToursProviders', on_delete=models.SET_NULL, null=True)

    name = models.CharField("Название экскурсии", max_length=128)
    description = models.TextField()
    price = models.DecimalField("Цена", decimal_places=2, max_digits=6, null=True)
    price_on_request = models.BooleanField('Цена по запросу', default=False)
    duration = models.PositiveIntegerField('Длительность, мин.', default=0)
    slots_str = models.TextField(blank=True, null=True)
    main_image = models.ImageField(upload_to=get_tour_main_image_path, null=True)
    max_participants = models.PositiveIntegerField('Максимальное количество человек на экскурсии', default=15)

    def __str__(self):
        return f"{self.name} {self.price} руб. / {self.duration} мин."

    @property
    def display_price(self):
        return f"{self.price} руб." if not self.price_on_request else 'Цена по запросу'

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"tour_id": self.id})



def get_tour_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<tour_id>/<filename>
    return f"d_{slugify(instance.tour.name)[:5]}/{filename}"


class TourImage(models.Model):

    tour = models.ForeignKey('tours.Tour', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_tour_images_path)


class Guide(models.Model):
    """Таблица гидов."""

    fio = models.CharField('ФИО гида.', max_length=64)
    phone = models.CharField('Телефон гида', max_length=16)

    def __str__(self):
        return f"{self.fio} ({self.phone})"


class Schedule(models.Model):
    """Расписание туров"""

    tour = models.ForeignKey('tours.Tour', on_delete=models.CASCADE)
    participant = models.ForeignKey('users.Participant', on_delete=models.SET_NULL, null=True)

    start_time = models.DateTimeField()

    def __str__(self):
        admin_format = '%d %B, %H:%M'
        return f"{self.participant.fio} на {self.tour.name} {self.start_time.strftime(admin_format)}"


