from django.core.management.base import BaseCommand

from tours.models import Tour
from tours_parser.models import ToursProviders
from tours_parser.parsers import parsers_by_label


class Command(BaseCommand):
    help = "Запустить все парсеры."

    def add_arguments(self, parser):
        parser.add_argument('providers_label', nargs='*')
        parser.add_argument('-r', default=False, nargs='?')

    def handle(self, *args, **kwargs):
        rewrite_db = kwargs.get('r') != False
        if rewrite_db:
            deleted = Tour.objects.all().delete()
            print("База данных очищена")
        providers_label = kwargs.get('providers_label', [])
        if not providers_label:
            providers = ToursProviders.objects.filter(is_active=True)
        else:
            providers = ToursProviders.objects.filter(label__in=providers_label, is_active=True)

        parsers = [(parsers_by_label.get(provider.label), provider) for provider in providers]
        for parser_class, provider in parsers:
            parser = parser_class(provider)
            print(f'Запуск парсера для {parser.label} из {parser.base_url}')
            parser.parse()


