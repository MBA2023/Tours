from django.db import models


class Participant(models.Model):
    fio = models.TextField()
    phone = models.CharField('Телефон участника экскурсии', max_length=16)

    def __str__(self):
        return f"{self.fio} ({self.phone})"
