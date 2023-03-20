import json

from app.models import Answer, Question, Test
from django.core.management.base import (BaseCommand, CommandError,
                                         CommandParser)
from quiz.settings import DATA_ROOT
from users.models import Color


class Command(BaseCommand):
    help = 'Загружает цвета в бд'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('filename', type=str)

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        filename = str(kwargs.get('filename'))
        try:
            with open(DATA_ROOT / filename, encoding='utf-8') as file:
                data = json.load(file)

            if filename == 'colors.json':
                for item in data:
                    Color.objects.get_or_create(
                        name=item['name'],
                        color=item['color'],
                        price=item['price'],
                    )

            if filename == 'tests.json':
                for item in data:
                    test_items = item['test']

                    test_obj = Test.objects.get_or_create(
                        title=test_items['title'],
                        coin=test_items['coin'],
                        points=test_items['points'],
                        description=test_items['description'],
                    )
                    for item in item['question']:
                        question_obj = Question.objects.get_or_create(
                            text=item['text'],
                            test=test_obj[0],
                        )
                        for item in item['answer']:
                            Answer.objects.get_or_create(
                                answer=item['answer'],
                                question=question_obj[0],
                                is_correct=item['is_correct'],
                            )
            print('== Успех! ==')

        except FileNotFoundError:
            raise CommandError(f'Файл {filename} отсутствует в каталоге data')
