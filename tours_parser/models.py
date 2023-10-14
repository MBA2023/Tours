from django.db import models


class ToursProviders(models.Model):
    """Источники туров."""

    name = models.CharField('Название источника', max_length=32)
    label = models.CharField('Лейбл источника', max_length=8)
    base_url = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {'Используется' if self.is_active else 'Не используется'}"