from django.core.management.base import BaseCommand, CommandError
from api.models import Genre


class Command(BaseCommand):

    help = "이 커맨드는 초기 genres 를 생성합니다."

    def handle(self, *args, **options):
        genres = ["K-POP", "발라드", "댄스", "R&B/SOUL", "락/메탈", "랩/힙합",
                  "일렉트로니카", "트로트", "인디", "블루스", "포크", "POP"]
        created_genre = []
        for name in genres:
            if Genre.objects.filter(name=name):
                continue
            else:
                Genre.objects.create(name=name)
                created_genre.append(name)
        self.stdout.write(self.style.SUCCESS(f"{len(created_genre)} Genres created!"))
