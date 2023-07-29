from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from tasktest.tasks import run_task


class Command(BaseCommand):
    help = "eat인자를 넣었을때 조건에 따라서 중복 실행되는 task를 테스트 합니다."

    def add_arguments(self, parser):
        parser.add_argument("sec", type=int, help="현재로 부터 Task 실행 시점(초)")
        parser.add_argument("name", type=str, help="Task에서 출력할 문자")

    def handle(self, *args, **options):
        name = options["name"]
        sec = options["sec"]

        exc_datetime = datetime.now() + timedelta(seconds=sec)
        run_task.apply_async([name], eta=exc_datetime)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully Excute Task name: {name} expected excute time: {exc_datetime}")
        )
